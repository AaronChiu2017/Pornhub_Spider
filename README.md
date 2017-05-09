# Pornhub_Spider

> 声明：本项目仅为本人学习Scrapy爬虫框架而用。他人请合理使用，并自行承担使用不当产生的后果。

### 简介

+ 项目主要是爬取全球最大成人网站PornHub的视频标题、时长、mp4链接、封面URL和具体的PornHub链接
+ 基于scrapy-redis和mongodb，数据存储在mongodb
+ 项目可以部署在docker上，利用分布式提高爬取速度

### 运行环境

Python2.7 

数据库：Redis，Mongodb

+ 需要在settings中修改redis_url和Mongodb_uri
+ Redis用于存储Requests队列和去重队列，供分布式爬虫食用
+ Mongodb用于存储item（视频相关信息）
+ start_requests由redis_key替换
+ 使用了随机cookies和UA，代码在middleware中。

启动：

+ python run_spider.py
+ 向redis数据库中`lpush pornHubSpider:start_requests https://xxxx`
+ 大概1小时爬取了1K+条信息

数据和结果：

+ Mongodb 中的PhRes表：

  ```
  video_title:视频的标题,并作为唯一标识.
  link_url:视频调转到PornHub的链接
  image_url:视频的封面链接
  video_duration:视频的时长，以 s 为单位
  quality_480p: 视频480p的 mp4 下载地址
  ```

  这些信息全部来自类似URL`https://www.pornhub.com/embed/ph58ff308e03243`的页面,其中ph58ff308e03243是视频的viewkey。

  页面中的js信息

  ```javascript
  var flashvars_vid608786924426529988 = {"disable_sharebar":0,"htmlPauseRoll":"false","htmlPostRoll":"false","embedCode":"<iframe src=\"https:\/\/www.pornhub.com\/embed\/ph58ff308e03243\" frameborder=\"0\" width=\"560\" height=\"340\" scrolling=\"no\" allowfullscreen><\/iframe>","autoplay":0,"autoreplay":"false","hidePostPauseRoll":"false","video_unavailable":"false","pauseroll_url":"","postroll_url":"","video_duration":"4526","actionTags":"","link_url":"https:\/\/www.pornhub.com\/view_video.php?viewkey=ph58ff308e03243","related_url":"https:\/\/www.pornhub.com\/video\/player_related_datas?id=114405431","image_url":"https:\/\/bi.phncdn.com\/videos\/201704\/25\/114405431\/original\/(m=eaAaGw-aaaaa)2.jpg","video_title":"               ","vcServerUrl":"/svvt/add?stype=evv&svalue=114405431&snonce=8j89sz3mf4waz472&skey=8327c3934552852d491a5b80e0fdf4c4a2d82d61d7ed9455b42f0859fc66952c&stime=1494328545","quality_480p":"https:\/\/ce.phncdn.com\/videos\/201704\/25\/114405431\/480P_600K_114405431.mp4?a5dcae8e1adc0bdaed975f0d60fb5e050d523df0cca6435032db1bab0a4b451d8a412585437d61ae6d91c700b28a32b0653892c2bcd8c75e85fe119c7f8fe2b639c1b80c6d196421f3dedeaa2e3880fb639b95a1dff9af68d0e9580294d927700eda711cf0634e4931ff6fcbc8724137578c932549c85e3cf377d8","video_unavailable_country":"false","toprated_url":"https:\/\/www.pornhub.com\/video?o=tr&t=m","mostviewed_url":"https:\/\/www.pornhub.com\/video?o=mv&t=m","browser_url":null,"morefromthisuser_url":"\/users\/hongtashan1956\/videos","options":"iframe","cdn":"edgecast","startLagThreshold":1000,"outBufferLagThreshold":2000,"appId":"1111","service":"","cdnProvider":"","mp4_seek":"ms","thumbs":{"samplingFrequency":9,"type":"normal","cdnType":"regular","urlPattern":"https:\/\/bi.phncdn.com\/videos\/201704\/25\/114405431\/timeline\/120x90\/S{20}.jpg","thumbHeight":"90","thumbWidth":"120"},"defaultQuality":[720,480,240,1080]};
  ```

  ​