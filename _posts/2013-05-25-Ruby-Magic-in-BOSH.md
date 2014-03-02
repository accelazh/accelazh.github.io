---
layout: post
category : BOSH
title : "Ruby Magic in BOSH"
tagline: "Ruby 元编程在BOSH中的运用"
tags : [BOSH, Ruby]
---

{% include JB/setup %}

最近研究Cloud Foundry与Openstack的集成功能，考虑到最终运用需要一个可支持动态部署的环境，因此选择了使用VMWare推荐的BOSH进行持续部署，
同时由于BOSH相关的文档非常有限，对于各种配置项的含义并没有专业的文档进行介绍，本着知其然要知其所以然的精神，对BOSH的代码进行了一些研究。
同时作为Ruby新手，在阅读中被Ruby动态编程特性所折服，学习了很多Ruby元编程的奇淫技巧，在此总结一二。

本文中多处比较ruby和java的实现差异，是为突出动态语言在处理一类问题的思考方式与静态语言的差异，而非比较语言本身优劣。特此声明，以免陷入无意义的语言之争。

## `class.send(:method,args)`

静态语言如Java如果想动态的调用一个类的一个方法，大概得这样写：

    Class myClass=Class.forName("package.to.MyClass");
    Object classInstance=myClass.newInstance(); 
    Method theMethod=myClass.getMethod("methodName", new Class[]{});
    theMethod.invoke();
    ...

作为动态语言的标志性特性，Ruby可以用`class.send(:method,args)`方法调用类的一切方法，同时配合`class.method_missing(method_name, *args)`方法使用，淋漓尽致地展现了动态语言的优美之处。一个例子的运用在于`agent_client`的代码实现中。

    module Bosh
      module Agent
        class BaseClient

          def run_task(method, *args)
            task = send(method.to_sym, *args)
            ...
            task
          end

          def method_missing(method_name, *args)
            result = handle_method(method_name, args)

            raise HandlerError, result["exception"] if result.has_key?("exception")
            result["value"]
          end

          protected
          def handle_method(method_name, args)
          end
        end
      end
    end

在部署过程中deployer会调用agent\_client与stemcell中的agent通信，命令agent做部署等其他操作，因此在deployer方大多就调用HTTPClient继承 自BaseClient的run\_task方法，然而由于大多数的请求都差不多，都是post\_json类型的请求，这里就通过send方法加上method\_misstiong方法来处理各种请求，当某个请求在开发过程中需要加入特殊行为时，再行加入该方法即可，降低了deployer与agent\_client之间的耦合。

这是一个非常基本的特性，这里列出只是为了在未来编程中更好地运用该特性

## `method_added(name)`

我的理解是`method_added(name)`是一种钩子方法，当module的继承类在定义方法后，ruby解释器会触发method_added事件，从而调用该方法做一些自定义的操作。
stackoverflow上有一个[问题的回答](http://stackoverflow.com/questions/4799760/understanding-method-added-for-class-methods)，也举例说明了这个问题。

    module Magic  
    	def	self.included(base)
    	    base.extend ClassMethods
    	end

        module ClassMethods
            def method_added(name)
                  puts "instance method '#{name}' added"
            end      

    	    def singleton_method_added(name)
    	          puts "class method '#{name}' added"
    	    end
    	end
    end
      
    classFoo  
    	include Magic

    	def bla
    	end  

    	def blubb
    	end  

    	def self.foobar
    	end
    end

Output

    instance method 'bla' added
    instance method 'blubb' added 
    class method 'foobar' added

有了这个简单的例子，我们来看看bosh_cli是如何实现响应用户的命令请求输入的

入口在`bosh_cli/bin/bosh`,其中就是调用`Bosh::Cli::Runner.run(ARGV.dup)`来响应。
在`Bosh::Cli::Runner.run(ARGV.dup)`中，代码如下：

    class Runner
    	def self.run(args)
          new(args).run
        end

        # @param [Array] args
        def initialize(args, options = {})
          @args = args
          @options = options.dup

          banner = "Usage: bosh [<options>] <command> [<args>]"
          @option_parser = OptionParser.new(banner)

          Config.colorize = true
          Config.output ||= STDOUT
        end

        # Find and run CLI command
        # @return [void]
        def run
        	...
          load_plugins
          build_parse_tree
    		...

          command = search_parse_tree(@parse_tree)
          
          ...

          command.runner = self
          begin
            exit_code = command.run(@args, @options)
            exit(exit_code)
          rescue OptionParser::ParseError => e
            ...
         end

        def build_parse_tree
          @parse_tree = ParseTreeNode.new

          Config.commands.each_value do |command|
            p = @parse_tree
            n_kw = command.keywords.size

            command.keywords.each_with_index do |kw, i|
              p[kw] ||= ParseTreeNode.new
              p = p[kw]
              p.command = command if i == n_kw - 1
            end
          end
        end
        ...
    end

看起来一切正常，静态方法run创建一个instance，然后调用instance的run方法，先建立命令处理的tree然后从中搜索输入的方法，然后run该方法。这里`build_parse_tree`中根据Config.commands中的value轮询一遍，建立树结构。但是当我去看Config.commands的时候，发现

    @commands = {}

是空的啊，程序顺序执行的话，这里还没什么方法往`@commands`里加K-V呢。那么程序是在什么时候往这个map结构种加入值的呢?只可能是类加载的时候。
从包和文件的命名规则来看，`lib/cli/commands/*.rb`肯定是最终处理请求的各种命令,且都继承自`Bosh::Cli::Command::Base`，而后者扩展了模块` Bosh::Cli::CommandDiscovery`. `Bosh::Cli::Command::Base`并没有什么特别的，定义了一些基本的操作，所有秘密都在`Bosh::Cli::CommandDiscovery`里：

    module Bosh::Cli
      module CommandDiscovery

        def usage(string = nil)
          @usage = string
        end

        def desc(string)
          @desc = string
        end

        def option(name, *args)
          (@options ||= []) << [name, args]
        end

        # @param [Symbol] method_name Method name
        def method_added(method_name)
          if @usage && @desc
            @options ||= []
            method = instance_method(method_name)
            register_command(method, @usage, @desc, @options)
          end
          @usage = nil
          @desc = nil
          @options = []
        end

        # @param [UnboundMethod] method Method implementing the command
        # @param [String] usage Command usage (used to parse command)
        # @param [String] desc Command description
        # @param [Array] options Command options
        def register_command(method, usage, desc, options = [])
          command = CommandHandler.new(self, method, usage, desc, options)
          Bosh::Cli::Config.register_command(command)
        end

      end
    end

定义了三个常量，但是有一个特殊的`method_added`方法，这下就全清楚了，在类加载的时候，当加入新的命令行处理方法时， 都会调用该方法搜集命令行处理方法，然后通过`register_command`将方法转换为`CommandHandler`的实例，然后调用`Bosh::Cli::Config.register_command`向`Bosh::Cli::Config`的@commands中注册。事实也确实如此，看`Bosh::Cli::Config.register_command`的代码如下

    def self.register_command(command)
          if @commands.has_key?(command.usage)
            raise CliError, "Duplicate command `#{command.usage}'"
          end
          @commands[command.usage] = command
    end

这样，任何一个想要扩展bosh命令从命令行执行的方法，只需要继承`Bosh::Cli::Command::Base`并加入一组处理方法就可以自动地向支撑的bosh所有命令行方法种注册了，示例如下

    usage "init release"
    desc "Initialize release directory"
    option "--git", "initialize git repository"
    def init(base = nil)
      ...
    end


这些用法/描述/选项和直接处理的方法，都被转换成一个`Bosh::Cli:CommandHandler`对象


    def initialize(klass, method, usage, desc, options = [])
      @klass = klass
      @method = method
      @usage = usage
      @desc = desc

      @options = options

      @hints = []
      @keywords = []

      @parser = OptionParser.new
      @runner = nil
      extract_keywords
    end

    # Run handler with provided args
    # @param [Array] args
    # @return [Integer] Command exit code
    def run(args, extra_options = {})
      handler = @klass.new(@runner)

      @options.each do |(name, arguments)|
        @parser.on(name, *arguments) do |value|
          handler.add_option(format_option_name(name), value)
        end
      end

      extra_options.each_pair do |name, value|
        handler.add_option(format_option_name(name), value)
      end

      args = parse_options(args)

      begin
        handler.send(@method.name, *args)
        handler.exit_code
      rescue ArgumentError => e
        say(e.message)
        err("Usage: #{usage_with_params}")
      end
    end

综上所述，如果需要扩展BOSH Cli的操作，只需要继承`Bosh::Cli::Command::Base`，依次调用`usage` `desc` `option`并定义实现方法，该方法就会在类加载的过程中自动被包装成`Bosh::Cli:CommandHandler`对象，并且以 K->usage V->CommandHandler的方式注册到`Bosh::Cli::Config`的@commands变量中，最终在执行时，调用包装后的CommandHandler实例的run方法，新建所定义的新命令行操作类的实例， 并调用相应的方法执行请求。事实上，`bosh_cli_plugin_aws`和`bosh_cli_plugin_micro`正是如此，将方法*自动*加入到Bosh命令行中，避免了对Bosh_cli代码的影响，方便扩展。

如果此类方法用java实现，可以通过反射机制加载所需要的对象，然后拼出对应的方法来执行，然而灵活性远比动态语言差。或许还有其他更好的方法

#END
















































