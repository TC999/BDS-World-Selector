# BDS-World-Selector
用于快速切换Minecraft 基岩版服务端存档工具

## 介绍

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">BDS-World-Selector</h3>

  <p align="center">
    一键修改 Minecraft 基岩版服务端(BDS)配置文件，不再为修改配置坐牢！
    <!--
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    -->
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/TC999/BDS-World-Selector/issues">反馈 BUG</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues/new?labels=enhancement&template=feature-request---.md">功能请求</a>
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>目录</summary>
  <ol>
    <li>
      <a href="#关于此项目">关于此项目</a>
      <!--ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
      -->
    </li>
    <li>
      <a href="#getting-started">快速开始</a>
      <!---
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
      -->
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#贡献">贡献</a></li>
    <li><a href="#许可证">许可证</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 关于此项目
这是一个用于可视化更改 BDS 配置文件的程序，用于快速切换存档，支持多存档不同设置，不再一个个手打！
本项目采用 ChatGPT4o 编写，代码质量一般，如有可优化空间，请直接提交拉取请求！

- 当前已实现更改：
    - [x] 服务器名
    - [x] 游戏模式
    - [x] 强制游戏模式
    - [ ] 种子更改
    - [ ] 最大在线人数

## 快速开始
暂无打算发布二进制文件，请使用源码运行

1. 安装 [Python](https://www.python.org)

2. git 克隆仓库到本地或直接下载 ZIP 压缩包
```
https://github.com/TC999/BDS-World-Selector.git
```

3. 将仓库内的`main.py`文件拷贝到您的 BDS 服务端目录下

4. 安装依赖
```python
pip install PyQt5
```

5. 运行 `main.py`

## 贡献
<!---
> [!IMPORTANT]
> 请提前设置GPG密钥，具体操作请查看[Github官方文档][github-doc-gpg-url]
-->
1. 复刻`(Fork)`此仓库
2. 创建一个分支`(Branch)`并以你修改的功能命名
3. 将代码拉到本地修改并提交`(Commit)`
4. 创建一个拉取请求`(Pull Request)`

## ✔ 待办(TODO)

- [ ] 更多选项
- [ ] 多语言适配（暂时只支持简体中文）
- [ ] 代码优化（GPT写的屎山）
- [ ] 每个存档单独配置文件

## 许可证
本项目采用 [GPL3 许可证](LICENSE)。