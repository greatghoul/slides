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

## commands

快捷键绑定

---

## identity

OAuth2

---

## storage

随 Google 帐户同步的数据存储

---

## pushMessaging

Google Cloud Messagin

---

## desktopCapture

桌面截图

---

## Cross Origin XHR 

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

## clipboard

访问系统剪贴板

---

## webRequest

分析和控制 Web 请求

---

## unlimitedStorage

打破 localStorage 5M 的限制

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
