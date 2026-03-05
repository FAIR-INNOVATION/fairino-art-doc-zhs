# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '法奥意威协作机器人用户手册'
copyright = '2022-2026, 法奥意威（苏州）机器人系统有限公司'
author = '法奥意威（苏州）机器人系统有限公司'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['recommonmark']

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'
locale_dirs = ['locale/']  # 设置本地化数据目录

# 让gettext为每个文档生成独立的.po文件（便于管理）
gettext_compact = False

# 支持的语言列表
language_options = {
    'zh_CN': '中文',
    'en': '英文',
    'ja': '日文',
}

# 添加语言切换器
html_context = {
    'display_languages': [
        ('zh_CN', '中文'),
        ('en', '英文'),
        ('ja', '日文'),
    ]
}

# source/conf.py

# 添加这些导入（放在文件开头）
from docutils.parsers.rst import Directive
from docutils import nodes
from docutils.parsers.rst import directives  # 这个也需要

# ... 你原有的其他配置 ...

# =========
# 多语言图片指令
# =========

class LangFigure(Directive):
    """多语言图片指令（带标题）"""
    
    required_arguments = 1  # 图片文件名
    optional_arguments = 0
    has_content = True  # 可以有标题
    
    # 支持所有 figure 指令的选项
    option_spec = {
        'align': directives.unchanged,
        'width': directives.length_or_percentage_or_unitless,
        'height': directives.length_or_percentage_or_unitless,
        'scale': directives.percentage,
        'alt': directives.unchanged,
        'class': directives.class_option,
    }
    
    def run(self):
        # 获取当前语言
        env = self.state.document.settings.env
        lang = env.config.language
        
        # 获取图片文件名
        img_file = self.arguments[0]
        
        # 根据语言构建图片路径
        if lang == 'zh_CN':
            img_path = f"image/zh_CN/{img_file}"
        elif lang == 'en':
            img_path = f"image/en/{img_file}"
        else:
            img_path = f"image/en/{img_file}"  # 默认英文
        
        # 创建 figure 节点
        figure_node = nodes.figure()
        
        # 创建图片节点
        img_node = nodes.image(uri=img_path)
        
        # 处理图片选项
        if 'alt' in self.options:
            img_node['alt'] = self.options['alt']
        else:
            img_node['alt'] = img_file
            
        for opt in ['align', 'width', 'height', 'scale']:
            if opt in self.options:
                img_node[opt] = self.options[opt]
        
        if 'class' in self.options:
            img_node['classes'] = self.options['class']
        
        figure_node += img_node
        
        # 处理标题（如果有）
        if self.content:
            caption_text = ' '.join(self.content)
            caption_node = nodes.caption(caption_text, caption_text)
            figure_node += caption_node
        
        return [figure_node]

def setup(app):
    # 注册多语言图片指令
    app.add_directive('limage', LangFigure)
    
    # 你可能有其他的 setup 代码
    # ...
# 注：在生成html的时候这句话要注释
# latex_engine = 'xelatex'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ["custom.css"]
html_logo = '_static/logo.svg'
html_theme_options = {
    'logo_only': True,
    # 'display_version': False,
    'language_selector': True,  # 显示语言切换器
}

# highlight_language = "c,c++,python"

# def setup(app):
#     app.add_css_file('_static/custom.css')

# rst_epilog = '\n.. include:: .custom-style.rst\n'