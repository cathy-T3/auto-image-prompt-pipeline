# auto-image-prompt-pipeline

把「提需表 → AI 提示词 → 车型参考图 → 出图」这条链路自动化的 Trae 技能包（skill）。

## 它能做什么

- 读取飞书提需表的一行（场景 / 车型 / 车色 / 数量）
- 按「70% 自写 + 30% AAA 模板骨架」生成 4K 竖版写实摄影提示词
- 按视角（左前 / 左后 / 右前 / 右后 / 纯侧 / 纯后 / 纯正）从车包中取车身参考图
- 在 TAI.lab 画布上严格按「上传 → 建节点 → 验证 → 连边 → 生图 → 轮询」顺序执行
- 下载结果并归档

## 安装

把本仓库放到 Trae 的用户级技能目录（目录名必须与 `SKILL.md` 的 `name` 一致）：

- 中国大陆版：`~/.trae-cn/skills/auto-image-prompt-pipeline/`
- 国际版：`~/.trae/skills/auto-image-prompt-pipeline/`

或项目级：`<workspace>/.trae/skills/auto-image-prompt-pipeline/`

## 目录结构

- `SKILL.md` — 技能入口，含触发条件与硬性约束
- `references/field-mapping.md` — 读表列映射、车包取图、角度判定
- `references/prompt-templates.md` — 换车 / 换场景 / 多车 提示词模板与负向提示
- `references/workflow.md` — TAI.lab 配置、API、严格执行顺序、连边排查、画布布局
- `references/pitfalls.md` — 踩坑清单
- `scripts/tailab_client.py` — 严格顺序 + 节点验证的 API 客户端示例
- `scripts/build_prompt.py` — 由提需行字段生成提示词的示例

## 使用

技能被触发后，按 `SKILL.md` 的「Core steps」执行，细节全部在 `references/` 下按需加载。
`scripts/` 中的示例脚本为可直接复用的确定性代码，运行前请在脚本里填入自己的 TAI.lab
JWT（从 workspace 的 `.tailab_config.json` 读取）。请勿把 token 提交进 Git。
