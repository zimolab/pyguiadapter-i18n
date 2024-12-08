import i18n
from pyguiadapter.action import Action
from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.menu import Menu
from pyguiadapter.utils import show_info_message
from pyguiadapter.widgets import (
    IntSpinBoxConfig,
    LineEditConfig,
    BoolBoxConfig,
    FloatSpinBoxConfig,
    ListEditConfig,
)
from pyguiadapter.window import BaseWindow, SimpleWindowEventListener
from pyguiadapter.windows.fnexec import FnExecuteWindowConfig

from pyguiadapter_i18n.config import Config, BASE_DIR, APP_CONFIG_FILE_PATH


def init_i18n():
    i18n.load_path.append(LOCALE_DIR)
    i18n.set("fallback", FALLBACK_LOCALE)
    i18n.set("file_format", "json")
    i18n.set("filename_format", "{namespace}.{locale}.{format}")
    i18n.set("enable_memoization", True)
    # i18n.set("error_on_missing_translation", True)
    i18n.set("skip_locale_root_data", True)  # IMPORTANT


LOCALE_DIR = BASE_DIR.joinpath("locales").absolute()
FALLBACK_LOCALE = "en"
LOCALE_NAMES = {
    "en": "English",
    "zh": "中文",
    "ja": "日本語",
}
init_i18n()
CONFIG_INSTANCE = Config.safe_load_from(APP_CONFIG_FILE_PATH)
i18n.set("locale", CONFIG_INSTANCE.language)


def foo(arg1: int, arg2: str, arg3: bool, arg4: float, arg5: list):
    pass


def on_set_locale(window: BaseWindow, action: Action):
    reversed_locale_names = {v: k for k, v in LOCALE_NAMES.items()}
    new_locale = reversed_locale_names[action.text]

    if new_locale == i18n.get("locale"):
        return

    i18n.set("locale", new_locale)
    CONFIG_INSTANCE.language = new_locale.lower()
    CONFIG_INSTANCE.save_to(APP_CONFIG_FILE_PATH)
    show_info_message(window, i18n.t("app.messages.lang_changed"))


action_locale_zh = Action(
    text=LOCALE_NAMES["zh"], on_triggered=on_set_locale, checkable=True
)
action_locale_en = Action(
    text=LOCALE_NAMES["en"], on_triggered=on_set_locale, checkable=True
)
action_locale_ja = Action(
    text=LOCALE_NAMES["ja"], on_triggered=on_set_locale, checkable=True
)


def on_window_create(window: BaseWindow):
    current_locale = i18n.get("locale")
    if current_locale == "zh":
        window.set_action_state(action_locale_zh, True)
    elif current_locale == "en":
        window.set_action_state(action_locale_en, True)
    elif current_locale == "ja":
        window.set_action_state(action_locale_ja, True)
    else:
        raise ValueError(f"Unsupported locale: {current_locale}")


def main():
    menu_lang = Menu(
        title=i18n.t("app.menu.lang"),
        actions=[action_locale_zh, action_locale_en, action_locale_ja],
        exclusive=True,
    )

    menus = [menu_lang]
    window_listener = SimpleWindowEventListener(on_create=on_window_create)
    window_config = FnExecuteWindowConfig(
        title=i18n.t("app.window.title"),
        execute_button_text=i18n.t("app.window.execute_button"),
        clear_button_text=i18n.t("app.window.clear_button"),
        function_result_message=i18n.t("app.messages.function_result"),
        output_dock_title=i18n.t("app.window.output_dock"),
        document_dock_title=i18n.t("app.window.document_dock"),
        default_parameter_group_name=i18n.t("app.window.default_param_group"),
    )
    widget_configs = {
        "arg1": IntSpinBoxConfig(
            label=i18n.t("app.widgets.arg1.label"),
            description=i18n.t("app.widgets.arg1.description"),
        ),
        "arg2": LineEditConfig(
            label=i18n.t("app.widgets.arg2.label"),
            description=i18n.t("app.widgets.arg2.description"),
        ),
        "arg3": BoolBoxConfig(
            label=i18n.t("app.widgets.arg3.label"),
            description=i18n.t("app.widgets.arg3.description"),
        ),
        "arg4": FloatSpinBoxConfig(
            label=i18n.t("app.widgets.arg4.label"),
            description=i18n.t("app.widgets.arg4.description"),
        ),
        "arg5": ListEditConfig(
            label=i18n.t("app.widgets.arg5.label"),
            description=i18n.t("app.widgets.arg5.description"),
            standalone_editor_button_text=i18n.t("app.widgets.arg5.edit_button"),
        ),
    }

    adapter = GUIAdapter()
    adapter.add(
        foo,
        window_menus=menus,
        window_listener=window_listener,
        window_config=window_config,
        widget_configs=widget_configs,
    )
    adapter.run()


if __name__ == "__main__":
    main()
