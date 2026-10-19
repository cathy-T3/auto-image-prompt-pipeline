# Prompt Templates

Write about 70% of the prompt yourself; use these only as the skeleton. Keep the car-body
image in position 图2 and always restate that 图2's body structure stays unchanged.

## Normal car swap (v20.7, current)

图1 = 提需参考图 (scene + car position + composition + original paint color).
图2 = 车包车身图 (car body design reference, at a given view angle).

```
3:4 竖版 4K 超高清写实摄影。
图1是提需参考图（{scene}场景+车辆位置+构图+原车漆色）；图2是{car}的车身设计参考图（{view}角度）。
必须保持图2车的车身结构、车身比例、车头设计、车灯造型、轮毂样式完全不变。
原封不动的将图2车的车身结构替换到图1车的位置上，保持图1场景完整不变，根据图1环境给图2车重新打光。
思考图1车漆颜色，将图1车漆顺着图2车身结构替换{color_clause}。
车辆拍摄角度必须与图2一致，不允许改变拍摄角度、朝向、透视。
画面中只允许出现一辆车，禁止出现背景车辆或多余车辆。
车身漆面真实反射图1场景的环境光影，自然光线，8K超高清写实摄影。
车型改为{car}
```

- `{color_clause}` → `，强制颜色为{color}` when the table specifies a color;
  otherwise `，颜色继承图1原车`.
- `{view}` is injected literally, e.g. 左前 / 右后.

## Earlier segmentation variant (v20.2) — for reference only

This form splits the instructions into 【角度锁定】/【场景锁定】/【车辆替换】blocks and uses
"第一张参考图 / 第二张参考图" wording. It is kept only to show the earlier 图2 = 车包 assumption.
Prefer the v20.7 natural-paragraph form above.

## Scene swap

图1 = 提需图 (scene source); 图2 = new background reference; 图3 = car-body reference.

```
3:4 竖版 4K 超高清写实摄影。
图1是提需参考图，包含原始场景、车辆位置和构图；图2是新的背景参考图；图3是{car}的车身设计参考图（{view}角度）。
原封不动的将图3车的车身结构替换到图1车的位置上，将图1车后的场景替换成图2，根据图2环境给图3车重新打光。
思考图1车漆颜色，将图1车漆顺着图3车身结构替换{color_clause}。
车辆拍摄角度必须与图1原本车辆完全一致，不允许改变拍摄角度、朝向、透视。
画面中只允许出现一辆车，禁止出现背景车辆或多余车辆。
车身漆面真实反射图2新场景的环境光影，自然光线。
{req}
```

Direction rule: the 提需图 is the scene source; the new scene is 图2. Do not keep the
Dongchedi scene and drop the body into it.

## Multi-car (two cars in one image)

序号-2 style: 左边车 + 右边车.

```
图1是提需参考图（含左右两辆车）；图2是{c1}的车身设计参考图（{view}角度）；图3是{c2}的车身设计参考图（{view}角度）。
必须保持图2车的车身结构和图3车的车身结构完全不变，禁止互相混淆车型。
原封不动的将图1左边的车替换为图2{c1}，右边的车替换为图3{c2}。
...
```

## Negative prompt

Base:

```
模糊，低质量，变形，扭曲，水印，文字，卡通，二次元，油画风格，多余车辆，多辆车，背景车辆
```

Extended (use this for car work):

```
模糊，低质量，变形，扭曲，水印，文字乱码，错别字，卡通，二次元，油画风格，
多余车辆，多辆车，背景车辆，懂车帝水印，懂车帝logo，黄色车牌，
改变车身外观，改变车头设计，改变前脸，改变车灯，
车型错误，品牌错误，混淆车型，串车型
```
