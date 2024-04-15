# evoldown-to-markdown
解析evoldown文件以兼容广泛存在的markdown解析器。

## 功能

- [ ] 解析evoldown文件为markdown文件。
  - [x] 识别学习材料类型标记并替换成对应的HTML代码
  - [ ] 识别 `^上标^` `~下标~` `==高亮==` `[!黑幕内容!]` 转换成对应HTML代码
- [ ] 生成文章导图

## 项目原理

就像[markdown作者博客](https://daringfireball.net/projects/markdown/#:~:text=%E2%80%9CMarkdown%E2%80%9D%20is%20two%20things%3A%20(1)%20a%20plain%20text%20formatting%20syntax%3B%20and%20(2)%20a%20software%20tool%2C%20written%20in%20Perl%2C%20that%20converts%20the%20plain%20text%20formatting%20to%20HTML)上说的：
> “Markdown”是两件事：（1）纯文本格式语法; （2）用Perl编写的软件工具，用于转换纯文本 格式化为 HTML。
