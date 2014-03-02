---
layout: post
title: "LOG : file upload/download in ajax style"
tagline : "日志 - 利用Ajax进行文件上传/下载"
description: "LOG : file upload/download in ajax style"
category: web-dev
tags: ["jquery","php"]
---
{% include JB/setup %}

最近为一个项目的Web页面添加文件上传/下载模块，其中用到了我认为最不优美的语言 javascript 和 php。此处记录一二。

## 背景

1. 本人对javascript和php的了解仅限于基本语法，纯newbee，也是借着这个机会学习，涉及的问题对于专业开发人员没什么难度，高手可以就此打住。

2. 由于深受REST风格的荼毒，将此功能设计为静态HTML网页 + REST API的方式来实现 - 将页面写成静态的HTML文件，与后台操作都通过Ajax请求REST API获取数据，达到页面和逻辑的分离。

3. 上传文件指上传特定文件(yaml)给server处理，然后返回处理结果(json), 下载指发送json数据，然后以文件方式(yaml)的返回处理结果。

4. 这里介绍的都是php最简实现，优雅的REST API不应该带.php类似的后缀

5. 这里介绍的方法和技巧不兼容IE旧版浏览器

开始

## 上传

### 选择文件

由于jquery没法直接调用浏览器打开文件选择器的接口，所以不得不借助 `<input type="file">`来实现。基本思想如下:

1. 用<div>确定一个类似button的位置
2. 在<div>上用 absolute 定位一个同样大小的`<input type="file">`, 盖在#1的div上。(可以用jquery动态调整大小)
3. 将`<input type="file">`的opacity设成0

这样用户看起来点在button上，实际上是触发了`<input type="file">`的文件选择器，就可以进行文件选择操作了。

代码:

  html:

    <a href="#" id="import_btn">IMPORT</a>
    <form id="upload_form" action="file_upload.php" method="post">
      <input type="file" id="import_file" style="overflow: hidden; opacity: 0; position: absolute;">
    </form>
  js:

    $('#import_file').css("width",$('#import_btn').width());
    $('#import_file').css("height",$('#import_btn').height());

### 上传文件

上传文件也就是提交input file所在的form，然而由于不存在submit按钮，用户也感受不到有这个input field的存在，这里我们通过监听input change event 采用ajax的方式提交。然而提交的是文件，而非普通的表单项目，这里用到`FileReader`来序列化文件，并且利用`FormData`对象作为ajax请求数据。

代码:
  
  js:

    $('#import_file').change(function(){
        var file = this.files[0];
        var name = file.name;
        var size = file.size;
        var type = file.type;

        if(file.name.length < 1 || file.size > 100000) { 
          //do nothing
        }else{
          if ( window.FileReader ) {
            reader = new FileReader();
            reader.readAsDataURL(file);
          }
          formdata = new FormData();
          if(formdata){
            formdata.append("data", file);
          }
        }
        $.ajax({ 
          url: 'file_upload.php',
          type: 'POST', 
          data:  formdata,
          processData: false,
          contentType: false,
          success: function(back){
            loadFromJSON(back); //do something with the request result
            $('#import_file').closest('form').get(0).reset();
          },
        });
    });

这里对文件进行简单检查后利用ajax提交。 `processData: false, contentType: false`如果不加的话php获取不到文件(求原因...)。
`$('#import_file').closest('form').get(0).reset();`重置input的值，防止当选择文件名不变时不触发change事件。

   file_upload.php 实现 REST API - POST /file_upload.php 

      <?php
        if($_SERVER["REQUEST_METHOD"] == "POST"){
          if($_FILES["data"]["error"] > 0){
            echo "Error: " . $_FILES["file"]["error"];
          }else{
            $yaml = yaml_parse_file($_FILES["data"]['tmp_name']) ;
            $json = json_encode($yaml);
            echo $json;
          }
        }      
      ?>

上传文件完成。

## 下载

由于安全因素，javascript不能直接下载文件，而且下载文件用POST请求有些不合适(幂等性)。此处借用了一个常见的思想分两步处理:

1. POST json 服务器端创建文件，返回一个id用于唯一标识该文件(考虑安全采用md5)
2. 用iframe来在原网页发送GET请求下载文件

实现：

* POST /files

  request {"foo":"bar"}

  response {"id":"foo-bar"}

* GET /files/foo-bar
   
  response yaml file

js:

    $('#export_btn').click(function(){
      $.ajax({
              type: "POST",
              url: 'files',
              data:  getJSONData(), //build the json data
              contentType: 'application/json', 
              dataType: 'json',
              success: function(retData) {
                        var url = 'files/' + retData.id ;
                        $("body").append("<iframe src='" + url +"' style='display: none;' ></iframe>");
                      },
            });
    });

form提交的默认contentType是`application/x-www-form-urlencoded`, 作为REST API请求必须把必须放在POST的body里（洁癖），所以需要设置成`application/json`。

php: 进行简单的md5校验防止安全问题的产生。
  
    <?php 
        define('TEMP_DIR', '/tmp/files/');

        if($_SERVER["REQUEST_METHOD"] == "POST"){
            $json = json_decode($HTTP_RAW_POST_DATA, true);
            $json = build_file_from_json($json);
            $yaml = yaml_emit($json);

            if(!file_exists(TEMP_DIR)){
              mkdir(TEMP_DIR, 0700);
            }
            $temp_name = tempnam(TEMP_DIR, "foo_");
            $temp = fopen($temp_name, 'w');
            fwrite($temp, $yaml);
            fclose($temp);
            $md5 = md5_file($temp_name);
            rename($temp_name, TEMP_DIR.$md5);

            $back = json_encode(array('id' => $md5));
            echo $back;

        }elseif($_SERVER["REQUEST_METHOD"] == "GET" && !is_null($_GET['id'])){
          $file_id = $_GET['id'];

          if(is_file(TEMP_DIR.$file_id) && is_readable(TEMP_DIR.$file_id) && md5_file(TEMP_DIR.$file_id) == $file_id){
            HttpResponse::setCache(true);
            HttpResponse::setContentType('application/octet-stream');
            HttpResponse::setContentDisposition($file_id, false);
            HttpResponse::setFile(TEMP_DIR.$file_id);
            HttpResponse::send();
            unlink(TEMP_DIR.$file_id);
          }else{
            echo "Error - No such file";
          }
          
        }
    ?>

这样的话就可以将文件下载至用户文件目录了，且`HttpResponse::setContentDisposition`第一个参数可以指定文件默认名称。


## 最后

由于对php和javascript的理解比较浅薄，所以做这个功能的时候查看了很多资料(stackoverflow我会说吗?)，解决了这些之前没处理过的问题。

对于PHP和JS的语法完全无爱，还是ruby更适合我的口味 :-）