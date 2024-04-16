# evoldown-to-markdown

evoldown-to-markdown是一个工具，用于解析evoldown文件为通用markdown文件，以兼容广泛存在的markdown解析器。

## 计划功能

- [ ] 解析evoldown文件为markdown文件。
  - [x] 识别学习材料类型标记并替换成对应的HTML代码
  - [ ] 识别 `^上标^` `~下标~` `==高亮==` `[!黑幕内容!]` 转换成对应HTML代码
  - [ ] 添加引导注意力的视觉效果
- [ ] 生成文章导图

## 项目原理

就像[markdown作者博客](https://daringfireball.net/projects/markdown/#:~:text=%E2%80%9CMarkdown%E2%80%9D%20is%20two%20things%3A%20(1)%20a%20plain%20text%20formatting%20syntax%3B%20and%20(2)%20a%20software%20tool%2C%20written%20in%20Perl%2C%20that%20converts%20the%20plain%20text%20formatting%20to%20HTML)上说的：
> “Markdown”是两件事：（1）纯文本格式语法; （2）用Perl编写的软件工具，用于转换纯文本 格式化为 HTML。

## 愿景

- evoldown-to-markdown能帮助到他人，
- 有代码高手提供更优秀的代码或贡献更方便衍生项目。 

## 里程碑

20240416，实现识别学习材料类型标记并替换成对应的HTML代码

当前，优化代码以便添加更多功能

## 起因

在项目开始的时候，渐构官网解析evoldown文件导出的HTML文件，在Hexo有显示异常的兼容问题。这影响了我对于自己笔记和文章的统一整理，便有了开发一个本地脚本的想法。

## 更新

冷瞳9I6：到目前为止，我还是一个外卖员，为了生存不能在这个项目里投入大量精力，暂时计划根据自己的实际需求逐渐改进项目。和很多开源项目一样，经济支持是项目更新动力。

## 作者官网

https://www.lt9i6.top