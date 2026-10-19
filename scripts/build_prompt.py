"""Build a 4K vertical photoreal prompt from one requirement row.

Mapping rules live in references/field-mapping.md; the template lives in
references/prompt-templates.md. Color is forced only when the table supplies
one, otherwise the reference-image color is inherited.
"""

NEG_PROMPT = (
    "模糊，低质量，变形，扭曲，水印，文字乱码，错别字，卡通，二次元，油画风格，"
    "多余车辆，多辆车，背景车辆，懂车帝水印，懂车帝logo，黄色车牌，"
    "改变车身外观，改变车头设计，改变前脸，改变车灯，"
    "车型错误，品牌错误，混淆车型，串车型"
)

TEMPLATE = """3:4 竖版 4K 超高清写实摄影。
图1是提需参考图（{scene}场景+车辆位置+构图+原车漆色）；图2是{car}的车身设计参考图（{view}角度）。
必须保持图2车的车身结构、车身比例、车头设计、车灯造型、轮毂样式完全不变。
原封不动的将图2车的车身结构替换到图1车的位置上，保持图1场景完整不变，根据图1环境给图2车重新打光。
思考图1车漆颜色，将图1车漆顺着图2车身结构替换{color_clause}。
车辆拍摄角度必须与图2一致，不允许改变拍摄角度、朝向、透视。
画面中只允许出现一辆车，禁止出现背景车辆或多余车辆。
车身漆面真实反射图1场景的环境光影，自然光线，8K超高清写实摄影。
车型改为{car}"""


def normalize_car(car):
    c = car.strip()
    for prefix in ("沃尔沃 ", "沃尔沃", "Volvo ", "Volvo"):
        if c.startswith(prefix):
            return c[len(prefix):].strip()
    return c


def build_prompt(scene, car, color=None, view="左前", req=""):
    """Return a prompt for one image. `color` falsy -> inherit reference color."""
    color_clause = f"，强制颜色为{color}" if color else "，颜色继承图1原车"
    prompt = TEMPLATE.format(
        scene=scene.strip(),
        car=normalize_car(car),
        view=view.strip(),
        color_clause=color_clause,
    )
    return f"{prompt}\n{req.strip()}" if req else prompt


if __name__ == "__main__":
    print(build_prompt("户外", "沃尔沃EM90", color="黑色", view="左后"))
