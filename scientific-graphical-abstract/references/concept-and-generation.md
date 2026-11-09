# 构思与图像生成

## 1. 读材料而非猜机制

建立简短的“标签/关系 → 来源位置 → 证据级别”表。来源可以是正文、图注、PPT 页、用户明确补充；若只收到一张已确认总图，就以图为内容母版并说明未重新审阅全部实验。

特别区分：

- 功能效应与直接结合；对接预测与靶点确证。
- 相关变化与因果通路；核定位与转录活性。
- 微环境/材料支撑与外源机械加载。
- 修复形态、骨量和力学质量；不要把一种读出扩成另一种结果。
- 人数据参考桥接、动物模型和细胞实验的边界。

不要编造数据、比例尺、组织学照片、结构解析、显著性标记或数值。图示科学插画不能伪装为实验图像。

## 2. 设计可读的核心故事

常用但不强制的结构：问题微环境 → 主机制 → 干预与功能结果，辅以上方短证据链。整体应形成一个连贯场景，而不是等宽卡片仪表板。

以研究创新为主视觉，不以所有检测方法清单为主视觉。保留用户要求的全部内容，但可通过更短标签、次级说明和分级信息降低拥挤。
有组织—细胞放大时用清晰的放大框/引线，不能把组织直接画成细胞膜延续。材料释放与机械支持的箭头分开，避免一个箭头承载多个含义。

若要做 AFM 小型 ToC 版，另做精简构图，不压缩完整机制总图；未要求额外版本时先说明必要性或仅提供当前版。

## 3. 搜索与风格参考

用户要求检索或要求具体期刊规则时，查官方投稿指南、出版商文章及图稿指南。技术操作同样优先官方文档。
参考文章图的构图/文字层级可以借鉴，但不复制其独特科学内容，不捏造“某期刊统一风格”。保留实际使用链接及核对日期。

官方入口示例（使用时再次核验）：

- AFM: https://advanced.onlinelibrary.wiley.com/hub/journal/16163028/author-guidelines
- Nature: https://research-figure-guide.nature.com/
- Nature Aging: https://www.nature.com/nataging/submission-guidelines

GitHub 提示词/技能只能辅助设计，不能替代实验依据；检索不等于授权安装任意仓库。

## 4. 图像生成提示词结构

每个输入图都明确标注角色：内容母版、用户手改母版、风格参考、需保留的局部素材。先查看本地图片，再传给支持该输入机制的绘图工具。

可复用提示词框架（填具体信息，不把占位符交给生成器）：

```text
Task: original scientific graphical abstract / targeted style-transfer edit.
Content master: [source]; style-only reference: [reference].
Preserve: [approved content, exact labels, relationships and current edits].
Core conclusion: [one defensible sentence].
Composition: [primary scene, supporting evidence chain, tissue/cell scale transitions].
Scientific relationships: [measured versus proposed; arrows and their directions].
Exact labels: [verified strings, capitals, Ca2+ or other superscripts].
Visual treatment: editorial scientific illustration, restrained matte shading,
organic anatomy, controlled contours, clean consistent sans-serif typography.
Palette: [small palette aligned with the current study/artwork].
Avoid: plastic highlights, glossy beads, 3D buttons, metallic arrows, decorative
banners, repeated icon cards, noisy texture beneath text, invented structures/data.
Output: [aspect ratio, full figure or background only, native high resolution].
```

“去生成感”不是把所有插画换成几何图标。根据参考图保留有用的解剖形态和支架细节，减少不必要的皮肤/烟雾纹理、过度高光及模板感。

使用当前可用 GPT 内置图像工具，必要时按其 imagegen 技能执行。不能仅因想控制保存路径、分辨率或批量就私自切换付费 API/CLI。版本不透明则明确标注未核验。

## 5. 迭代与原始记录

每次只聚焦主要问题：结构/内容 → 画风 → 标签与箭头 → 投稿规格。不要在用户只要求风格时悄悄改科学结论。
用户手改后，以最新手改版为母版；只有截图时可以做风格或背景辅助，但不能声称保存了其全部原生图层。
保存原始生成结果与完整提示词，不覆盖用户源文件，不把放大插值称为新增原生细节。不保证生成模型精确遵守每条提示词，必须视觉检查输出。
