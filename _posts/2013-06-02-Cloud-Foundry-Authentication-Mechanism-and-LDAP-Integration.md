---
layout: post
title: "Cloud Foundry Authentication Mechanism and LDAP Integration"
tagline: "Cloud Foundry 认证机制与LDAP集成"
description: "Cloud Foundry Authentication Mechanism"
category: cloudfoundry
tags: [Cloudfoundry, Authorization, LDAP]
---
{% include JB/setup %}

本文简要介绍Cloud Foundry的用户认证过程，以及相关项目组件，并介绍同企业LDAP认证集成的方法。碍于篇幅，本文将众多代码和配置文件信息用github链接的方式给出，具体到行，请辅助查阅。

## Cloud Foundry 认证

Cloud Foundry 作为如今炙手可热的开源项目，借助其可以方便搭建企业内部PaaS平台，然而在集成时首先遇到的问题就是同企业内部系统中的授权系统（如LDAP）集成。与认证活动的相关的组件，主要有以下4个：

1. **vmc** : 
V1版客户端，由于V2近期将release，将采用cf客户端，但原理和功能与vmc一样，vmc是一个Ruby项目，代码见 <https://github.com/cloudfoundry/vmc>
(**vmc-0.5.1已经可以正常工作**)
2. **cloud_controller** :
VCAP的控制组件V1版本，主要功能是告知客户端(vmc)进行用户认证请求的地址，并且根据用户TOKEN请求UAA认证。cloud\_controller是一个ROR项目，代码见 <https://github.com/cloudfoundry/cloud_controller>
3. **uaa** :
用户认证模块，Cloud Foundry进行用户管理/认证的核心模块，后台DB保存用户信息，对外提供多种认证接口，如[OAuth 2][2]和[SCIM][4]，以及[JWT][3]格式的支持。uaa是一个Java Spring项目，代码见 <https://github.com/cloudfoundry/uaa>
4. **login-server** : 
如果需要额外的外部授权方式以及定制登录页面，可采用login-server进行，只进行授权，不进行用户管理，无db保存用户数据。login-server是一个Java Spring项目，代码见 <https://github.com/cloudfoundry/login-server>

认证系统的发展史随着Cloud Foundry的发展逐渐成熟起来的。

起初，Cloud Foundry的认证系统也从最初的在Cloud Controller组件中，用户将用户名和密码存在Cloud Controller 的数据库中，当登录时提供用户名和密码，并获取一个token，后续操作需要提供token进行验证后方能进行，如图所示：

![Cloud Foundry Authentication - 1][1]

进而增加了UAA (User Account and Authentication) 组件和ACM (Access Control Management)专门用于用户认证和访问控制(后者本文暂不涉及)，UAA采用多种开放的标准协议，支持[OAuth][4]验证，TOKEN采用标准的[JWT(JSON Web TOKEN)][5]格式封装，并对外开放[SCIM(System for Cross-domain Identity Management)][6]接口进行用户操作。在此基础上，需要授权与认证的组件就相当于OAuth验证的活动参与者，VMC作为客户，Cloud Controller作为第三方客户端，UAA则扮演服务提供方的角色，同时基于Cloud Foundry开发的系统也可以通过OAuth协议请求UAA授权和认证。此时结构如图所示：

![Cloud Foundry Authentication - 2][2]

然而，在私用云中往往涉及外部认证的场景，一方面来自企业认证(LDAP等方法)的用户在登录时需要能够进行外部验证以保证用户身份，另一方面用户在访问cloud foundry时需要能够继续通过UAA进行认证，为此又加入了login-server组件来支持外部授权，同时作为UAA的一个特殊客户端，可以申请UAA的TOKEN。最终形成了一个支持扩展的认证组件集合，如图所示。

![Cloud Foundry Authentication - 3][3]

## 认证过程

如上图所示，认证过程参与者众多，登录的流程简单来说包含图中所示的10个步骤：

1. **vmc -> cloud_controller : GET /info** 
   
   在返回的JSON信息中包括`"authorization_endpoint": "http://login.cf.com"`,vmc会根据此信息申请验证

2. **vmc -> login-server: GET /login**
 
   此处是请求login-server获取需要验证的信息的提示，如
   `"prompts": { "username": [ "text", "Email" ], "password": [ "password", "Password" ] }`

    该提示信息的处理逻辑在`org.cloudfoundry.identity.uaa.login.RemoteUaaController`中，根据`prompts`属性，首先选取`prompts`属性，如果没有被设定，则请求UAA uaaBaseUrl(配置项中的`uaa.url`见[代码][11])，如果请求失败，则采用默认值Email+Password，相关代码见[RemoteUaaController#getLoginInfo][12]。如果要修改提示信息，可以在spring-servlet.xml中注入属性值，或调整最后默认值。

3. **vmc -> login-server : POST /oauth/authorize?client\_id=vmc&response\_type=token**
   
   vmc根据先前获取的prompts信息提示用户输入用户名/密码，在请求body中包括了类似验证信息`credentials={"username":"foo","password":"bar"}`，对于vmc-0.5.1及之后的版本包含的验证信息为`username=foo&password=bar&source=credentials`,处理过程和前者一致

4. **login-server -> ldap**
	
   login-server对ldap和OAuth的请求和验证是通过Spring Security实现的。对应的filter是[AuthzAuthenticationFilter][15]([spring配置][13])，会根据spring_profile确定是直接使用uaa的oauth验证还是请求外部验证。对于ldap类型的验证，将采用[UsernamePasswordExtractingAuthenticationManager][16]进行([spring配置代码][14])，实际还是通过`org.springframework.security.ldap.authentication.LdapAuthenticationProvider`代理来进行实际的LDAP验证。如果验证成功，进入[RemoteUaaController#startAuthorization][17]进行响应。

5. **login-server -> uaa : POST /oauth/authorize?client\_id=vmc&response\_type=token&source=login&username=foo**
   
   请求的消息体在[RemoteUaaController#startAuthorization][17]中组装，通过`org.springframework.security.oauth2.client.OAuth2RestTemplate`发送请求，设置在[spring配置][18]中.HTTP body中包含

   `[{response_type=[token], redirect_uri=[https://uaa.cloudfoundry.com/redirect/vmc], client_id=[vmc], source=[login], username=[foo]}]`

   表示源请求来自vmc，由login-server向uaa请求验证，用户名为foo

6. **uaa -> uaa-db -> login-server**

   uaa也是利用Spring Security实现的认证和授权功能。请求中包含`source=login`向uaa声明来源来自login-server，被声明在login-server-security.xml中的[loginAuthorizeRequestMatcher][19]命中，这里声明了两个filter

   		<custom-filter ref="oauthResourceAuthenticationFilter" position="PRE_AUTH_FILTER" />
		<custom-filter ref="loginAuthenticationFilter" position="FORM_LOGIN_FILTER" />

   前者声明为org.springframework.security.oauth2.provider.error.OAuth2AuthenticationEntryPoint的filter，在uaa.yml中配置了Login-server应具有的权限操作_oauth.login_ 
   后者是[AuthzAuthenticationFilter][15]的一个实例，会从request中抽取用户的username，将实际的认证操作代理给[loginAuthenticationMgr][21]中，声明为[LoginAuthenticationManager][21]的一个实例，根据[spring配置][22]，传入两个重要参数，其中”addNewAccounts“用于判断是否在用户不存在时根据Login传入的用户信息新建用户，对应`uaa.yml`中的`login.addnew`的值，”userDatabase“则根据配置文件中的database信息代理uaa-db的操作。

   在[LoginAuthenticationManager#authenticate][21]中，代码如下

	   	@Override
		public Authentication authenticate(Authentication request) throws AuthenticationException {

			if (!(request instanceof AuthzAuthenticationRequest)) {
				logger.debug("Cannot process request of type: " + request.getClass().getName());
				return null;
			}

			AuthzAuthenticationRequest req = (AuthzAuthenticationRequest) request;
			Map<String, String> info = req.getInfo();

			logger.debug("Processing authentication request for " + req.getName());

			SecurityContext context = SecurityContextHolder.getContext();

			if (context.getAuthentication() instanceof OAuth2Authentication) {
				OAuth2Authentication authentication = (OAuth2Authentication) context.getAuthentication();
				if (authentication.isClientOnly()) {
					UaaUser user = getUser(req, info);
					try {
						user = userDatabase.retrieveUserByName(user.getUsername());
					}
					catch (UsernameNotFoundException e) {
						// Not necessarily fatal
						if (addNewAccounts) {
							// Register new users automatically
							publish(new NewUserAuthenticatedEvent(user));
							try {
								user = userDatabase.retrieveUserByName(user.getUsername());
							}
							catch (UsernameNotFoundException ex) {
								throw new BadCredentialsException("Bad credentials");
							}
						}
						else {
							throw new BadCredentialsException("Bad credentials");
						}
					}
					Authentication success = new UaaAuthentication(new UaaPrincipal(user), user.getAuthorities(),
							(UaaAuthenticationDetails) req.getDetails());
					publish(new UserAuthenticationSuccessEvent(user, success));
					return success;
				}
			}

			logger.debug("Did not locate login credentials");
			return null;

		}

   代码很简单，首先验证传入请求的类型是否是AuthzAuthenticationRequest并确认是OAuth2类型的验证，根据请求中包含的user信息，要求name和email字段至少二者有其一，如果name为null，则将email作为name，反之如果email为null，则根据name中是否包含@进行判断，如果包含,email=name，否则email=name@unknown.org，而givenName和familyName如果不存在，则分别取email字段的@前后两部分，[具体代码见此][23]。之后查询uaa-db中是否包含username=foo的用户，如果找到则返回验证成功。否则如果允许添加新用户，则发布新增用户的事件，由[ScimUserBootstrap][24]负责处理事件，新增用户，当用户添加成功后返回验证成功，否则验证失败。

   简单介绍一下UAA中的事件机制，这里新增用户和记录Log等操作都基于Spring的事件机制，uaa项目内部总共有三类事件，[AbstractUaaEvent][25] + [AuthenticationFailureBadCredentialsEvent][26] (Spring的事件，UAA监听用于发布AbstractUaaEvent的事件实例以便log) + [NewUserAuthenticatedEvent][27] ，分别对应三个Listener [AuditListener][28] + [BadCredentialsListener][29] + [ScimUserBootstrap][24]。SCIM在提供用户操作的REST标准接口之外，也监听新建用户的事件。其中AbstractUaaEvent主要利用[JdbcFailedLoginCountingAuditService][30]和[LoggingAuditService][31]，前者监听UserAuthenticationSuccess/PasswordChangeSuccess/UserAuthenticationFailure当用户登录后修改密码或登录失败时操作sec_audit表删除认证信息，后者则进行log的管理和统计记录等功能，NewUserAuthenticatedEvent则仅仅用户新建用户。
 
   当通过这些Filters验证后，由org.springframework.security.oauth2.provider.endpoint.AuthorizationEndpoint.authorize进行一番查询操作后返回token信息。

7. **login-server -> vmc ->.vmc**
	
	login-server将token返回给vmc, vmc将其记录在~/.vmc/tokens.yml中。除token外还包括token类型、超时时间和JTI(JSON web Token Id)

	`token_type=bearer&expires_in=604799&jti=1815ccfe-68a4-4d1d-a16a-2eff55622002`

8. **vmc -> cloud_controller : GET /apps**

	当用户对cloud controller进行操作时(以/apps请求为例)，vmc在HTTP HEAD中包含token信息

	`authorization : bearer [tokens]`

9. **cloud\_contorller -> uaa : GET /token\_key**
	
	cloud controller是一个典型的ROR工程，在所有的Controller都继承自ApplicationController，其中的`before_filter :fetch_user_from_token`将验证用户的TOKEN，首先需要解码token
	+ 验证token，根据uaa.url和uaa.client_secret发送请求到uaa，获取token key
	+ 根据token信息解码，根据token_key解码token，获取user的email
 
10. **cloud_contorller -> cc-db -> vmc**

	然后查询cc-db确定用户，查询token中包含的用户名是否在cc-db中存在，如果存在继续由对应请求的Controller处理，如 GET /apps由AppsController处理，具体的路由规则可以在config/routes.rb中查看

	这里存在一个问题，当用户是通过`vmc register`方法注册用户时，会请求 POST /users 来创建用户，在UsersController中会根据uaa的配置在uaa和cc-db中创建用户，之后登录时能够通过uaa验证，发送其他请求时ApplicationController可以在cc-db中查找到用户，因而请求可以正常进行。
	然而如果用户是从LDAP导入到UAA中去的，省去了注册环节，用户是在login-server向UAA请求token时加入uaa-db的，但cc-db中并没有该用户的数据，在这一步根据email查找用户时会失败，所以返回401错误。同时这里cloud controller查找用户并没有特殊的含义，只是记录用户访问cloud controller的时间(当使用uaa时cc-db的active字段都是false)，并不通过该记录验证任何消息。

	因此我们进行了如下的代码调整。

## 代码调整

相关的代码调整增加对应本人fork cloud_controller的repo中，<https://github.com/TieWei/cloud_controller/commit/49fc960330dc881adc199021b33c9c83d25fd85e>

	if (!user_email.nil?)
	CloudController.logger.debug("user_email decoded from token is #{user_email.inspect}")
	@current_user = ::User.find_by_email(user_email)
		if @current_user.nil? && uaa_enabled?
		  CloudController.logger.debug("#{user_email.inspect} from uaa is not in CloudController DB, Try to create a proxy one")
		  user = ::User.new :email => user_email
		  # the password is encrypt with (user_email + current time) 
		  user.set_and_encrypt_password(user_email + Time.now.to_s) 
		  if user.save
		    @current_user = ::User.find_by_email(user_email)
		    CloudController.logger.info("proxy user #{user_email.inspect} from uaa is added into CloudController DB")
		  else
		    @current_user = nil
		    CloudController.logger.warn("proxy user #{user_email.inspect} from uaa is not added into CloudController DB")
		  end
		end
	end

如果用户不存在，且采用UAA的方式进行验证，则根据用户的email和当前时间生成一个代理用户(只用于让cloud controller知道该用户存在)，并存入cc-db中。

实现虽然略显dirty，但是总归是能work了。

另外，如果选用vmc-0.5.1版本的客户端，请求login-server时附带的body中包含的信息是`username=foo&password=bar&source=credentials`，这里在login-server请求处理`/oauth/authorize`时会有一点安全隐患 -- login-server会将用户的密码存入log (log级别是debug时)并发送给uaa，当采用外部认证的场景时，用户的密码或许会因为login-server的log而被利用。此处代码全部代码在[RemoteUaaController][32]中，关键片段如下：

	if (principal != null) {
			map.set("source", "login");
			map.setAll(getLoginCredentials(principal));
			map.remove("credentials"); // legacy vmc might break otherwise
		}

当请求是`credentials={"username":"foo","password":"bar"}`时，用户密码信息会被删除，然而0.5.1版本时则不会删除，解决办法很简单，加一行
`map.remove("password");` 即可。

 
## 配置选项

* 使用cloud controller的master分支，最新版加入了login-server的支持，[关键代码在此][7]

* 使用 cloudfoundry-identity-uaa-1.4.1.war ，理论上login-server的spring\_profile中有ldap即可，[关键代码在此][8]

* 使用 cloudfoundry-login-server-1.2.1.war，uaa有login-server-security.xml响应来自login-server的请求即可，[关键代码在此][9]。

* 编辑`login.yml`，设定如下

		spring_profiles: ldap
		ldap:
		  base:
		    url: 'ldap://your.domain.com:389/dc=domain,dc=com'
		    userDnPattern: 'CN={0},ou=Employees, ou=Users' 

  PS: 默认的userDnPattern是`uid={0},ou=people`,如果需要调整(如上设定)，需编辑[此处代码][10]为
  `<value>${ldap.base.userDnPattern:uid={0},ou=people}</value>`

* 如果需要从LDAP向UAA导入用户，需要编辑`uaa.yml`，设定如下

	    login
	  	  addnew: true

这样，Cloud Foundry就可以正确将用户登录信息向LDAP请求验证。

---

## Reference:

1. [OAuth 2][4] - token based authentication for web applications and APIs. Defines the client software as a role. Separates issuing tokens from how you use a token. Token issuance is defined both for browsers and for REST clients using a username/password. Token format is not defined by OAuth2, but one proposed standard format is JWT.

2. [JWT][5] - JSON Web Tokens, an upcoming standard format for structured tokens (containing data) which are integrity protected and optionally encrypted. 

3. [SCIM][6] - cross-domain user account creation and management. REST API for CRUD operations around user accounts 

4. <https://github.com/TieWei/uaa/blob/master/docs/UAA-CC-ACM-VMC-Interactions.rst>
5. <http://blog.cloudfoundry.com/2012/07/23/introducing-the-uaa-and-security-for-cloud-foundry>
6. <http://blog.cloudfoundry.com/2012/11/05/how-to-integrate-an-application-with-cloud-foundry-using-oauth2>
7. <http://blog.cloudfoundry.com/2013/02/19/open-standards-in-cloud-foundry-identity-services>
8. <http://blog.cloudfoundry.com/2012/10/09/securing-restful-web-services-with-oauth2>
9. <http://blog.cloudfoundry.com/2012/07/24/high-level-features-of-the-uaa>

# END

[1]: /images/CF-authorization-1.png "cloud-foundry-authorization-1"
[2]: /images/CF-authorization-2.png "cloud-foundry-authorization-2"
[3]: /images/CF-authorization-3.png "cloud-foundry-authorization-3"
[4]: http://oauth.net/2/ "oauth2"
[5]: http://self-issued.info/docs/draft-ietf-oauth-json-web-token.html "JWT"
[6]: http://www.simplecloud.info/ "SCIM"
[7]: https://github.com/cloudfoundry/cloud_controller/blob/master/cloud_controller/app/controllers/default_controller.rb#L14 "login-server-support"
[8]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L291 "login-server-ldap"
[9]: https://github.com/cloudfoundry/uaa/blob/master/uaa/src/main/webapp/WEB-INF/spring/login-server-security.xml#L34 "uaa-login-server-support"
[10]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L311 "login-server-userDnPattern"
[11]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L254 "login-server-uaa-base-url"
[12]: https://github.com/cloudfoundry/login-server/blob/master/src/main/java/org/cloudfoundry/identity/uaa/login/RemoteUaaController.java#L232 "login-server-prompts"
[13]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L188 "AuthzAuthenticationFilter-spring.xml"
[14]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L297 "ldap-profile"
[15]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/authentication/AuthzAuthenticationFilter.java#L111 "AuthzAuthenticationFilter"
[16]: https://github.com/cloudfoundry/login-server/blob/master/src/main/java/org/cloudfoundry/identity/uaa/login/UsernamePasswordExtractingAuthenticationManager.java#L47 "UsernamePasswordExtractingAuthenticationManager"
[17]: https://github.com/cloudfoundry/login-server/blob/master/src/main/java/org/cloudfoundry/identity/uaa/login/RemoteUaaController.java#L270 "RemoteUaaController"
[18]: https://github.com/cloudfoundry/login-server/blob/master/src/main/webapp/WEB-INF/spring-servlet.xml#L265 "uaa-oauth"
[19]: https://github.com/cloudfoundry/uaa/blob/master/uaa/src/main/webapp/WEB-INF/spring/login-server-security.xml#L20 "loginAuthorizeRequestMatcher"
[20]: https://github.com/cloudfoundry/uaa/blob/master/uaa/src/main/webapp/WEB-INF/spring/login-server-security.xml#L61 "loginAuthorizeRequestMatcher"
[21]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/authentication/manager/LoginAuthenticationManager.java#L62 "LoginAuthenticationManager#authenticate"
[22]: https://github.com/cloudfoundry/uaa/blob/master/uaa/src/main/webapp/WEB-INF/spring/login-server-security.xml#L73 "LoginAuthenticationManager-spring"
[23]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/authentication/manager/LoginAuthenticationManager.java#L117 "LoginAuthenticationManager#getUser"
[24]: https://github.com/cloudfoundry/uaa/blob/master/scim/src/main/java/org/cloudfoundry/identity/uaa/scim/bootstrap/ScimUserBootstrap.javaL139 "ScimUserBootstrap"
[25]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/audit/event/AbstractUaaEvent.java "AbstractUaaEvent"
[26]: https://github.com/SpringSource/spring-security/blob/master/core/src/main/java/org/springframework/security/authentication/event/AuthenticationFailureBadCredentialsEvent.java "AuthenticationFailureBadCredentialsEvent"
[27]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/authentication/manager/NewUserAuthenticatedEvent.java "NewUserAuthenticatedEvent"
[28]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/audit/event/AuditListener.java#L40 "AuditListener"
[29]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/authentication/event/BadCredentialsListener.java#L38 "BadCredentialsListener" 
[30]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/audit/JdbcFailedLoginCountingAuditService.java#L41 "JdbcFailedLoginCountingAuditService"
[31]: https://github.com/cloudfoundry/uaa/blob/master/common/src/main/java/org/cloudfoundry/identity/uaa/audit/LoggingAuditService.java#L92 "LoggingAuditService"
[32]: https://github.com/cloudfoundry/login-server/blob/master/src/main/java/org/cloudfoundry/identity/uaa/login/RemoteUaaController.java#280 "RemoteUaaController#startAuthorization"
