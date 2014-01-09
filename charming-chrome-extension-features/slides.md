title: 那些迷人的Chrome扩展特性
layout: true
theme: ../themes/gdg-xian/remark-gdg.css

---
name: first-page
class: center, middle

<img src="../themes/gdg-xian/gdg.png" width="50%" />

<img src="../themes/gdg-xian/gdg-xian-large.png" width="80%" />

### 西安谷歌开发者社区

---
class: center, middle

<img src="../themes/gdg-xian/gdg-xian-icon.png" />

<h2 style="color: #ff5447;">热烈欢迎你来参加</h2>
<h2 style="color: #ff5447;">西安 GDG 社区交流活动！</h2>

---
class: center, middle

# 那些迷人的 Chrome 扩展特性
[greatghoul@GDG西安201401]

---

## #1 commands

 * 支持 A-Z, 0-9, Arrow keys 及很多其它的控制键  
 * 所以快捷键必须和 **Ctrl** 或 Alt 组合使用
 * Chrome 原生的快捷键优秀级高于扩展快捷键，且不能被覆盖
 * 适应不同平台 default / windows / mac / chromeos / linux
 * 扩展预留 `_execute_browser_action` 和 `_execute_page_action`
 * 用户可以在扩展页面中自己定义快捷键

---

  "commands": {
    "toggle-feature-foo": {
      "suggested_key": {
        "default": "Ctrl+Shift+Y",
        "mac": "Command+Shift+Y"
      },
      "description": "Toggle feature foo"
    },
    "_execute_browser_action": {
      "suggested_key": {
        "windows": "Ctrl+Shift+Y",
        "mac": "Command+Shift+Y",
        "chromeos": "Ctrl+Shift+U",
        "linux": "Ctrl+Shift+J"
      }
    },
  },

---

响应快捷键的触发事件

    chrome.commands.onCommand.addListener(function(command) {
      console.log('Command:', command);
    });

---

<!-- TODO: 添加扩展快捷键自定义的截图 -->

---

## #2 identity

内置的 OAuth2 库

 * 近水楼台先得月，访问自家 Google OAuth2 非常方便
 * 对于第三方的 OAuth2，需要使用标准流程
 * Chrome 自动缓存 access token 并代理其过期操作

.footnote[Sine 19]

---

## #3 storage

针对 Chrome 扩展而优化的数据存储功能

 * 随 Google 帐户同步的数据存储
 * 可以直接在 content scripts 中直接访问
 * 读写都是异步进行，响应更快，当然也带来一些不便
 * 数据可以存储为对象，而非字段串
 * 可以定义要存储的数据的格式以严格验证
 * 可以监听 storage 的变化
 * local / sync / managed

---

预定义的格式

manifest.json

    "storage": {
      "managed_schema": "schema.json"
    },

schema.json

    {
      "type": "object",
      "properties": {
        "AutoSave": {
          "title": "Automatically save changes.",
          "description": "If set to true then changes will be automatically saved.",
          "type": "boolean"
        },
        // ...
      }
    }

---

## #4 pushMessaging

Google Cloud Messagin

---

## #5 desktopCapture

桌面截图

---

## #6 Cross Origin XHR 

 * 基于 **pattern** 的白名单的跨域 XHR
 * 请求扩展内部资源
 * 避免直接 eval 脚本或 html
 * Content Security Policy (CSP)

---

manifest.json

    "permissions": [
      "http://www.google.com/",
      "https://www.google.com/"
    ]

Background.js

    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://api.example.com/data.json", true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4) {
        // JSON.parse does not evaluate the attacker's scripts.
        var resp = JSON.parse(xhr.responseText);
      }
    }
    xhr.send();

---

## #7 clipboard

访问系统剪贴板

---

## #8 webRequest

 * 监听HTTP请求的执行状态
 * 修改请求 cancel / rredirect / headers (limited) / auth 
 * 修改请求需要额外的权限 **webRequestBlocking**
 * 更快的 declarativeWebRequest (beta and dev)

.footnote[Since 17]

---

## alarms

浏览器上的定时任务

---

## Event Pages

 * Chrome 22+ 
 * 只在必要时才加载
 * Alarms 替代 setTimout 和 setInterval
 * Event Pages v.s. Background Pages

---

Background Pages:

    {
      "name": "My extension",
      ...
      "background": {
        "scripts": ["background.js"]
      },
      ...
    }

---

Event Pages:

    {
      "name": "My extension",
      ...
      "background": {
        "scripts": ["eventPage.js"],
        "persistent": false
      },
      ...
    }

---
name: last-page
class: center, middle

<img src="../themes/gdg-xian/gdg.png" width="50%" />

# 开放 分享 创新

## [developers.google.com](http://developers.google.com)
