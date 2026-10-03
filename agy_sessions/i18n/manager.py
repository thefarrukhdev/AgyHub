import os
import json
from typing import Optional
from agy_sessions.core.config import CONFIG_FILE
from agy_sessions.i18n.translations import TRANSLATIONS

CURRENT_LANG = 'en'

def load_language(cli_lang: Optional[str] = None):
    global CURRENT_LANG
    
    # 1. CLI arg explicitly overrides and saves
    if cli_lang in TRANSLATIONS:
        CURRENT_LANG = cli_lang
        try:
            CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'lang': CURRENT_LANG}, f)
        except Exception:
            pass
        return

    # 2. Config file
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                conf = json.load(f)
                if conf.get('lang') in TRANSLATIONS:
                    CURRENT_LANG = conf['lang']
                    return
    except Exception:
        pass

    # 3. Auto-detect from env var
    lang_env = os.environ.get('LANG', '').lower()
    if lang_env.startswith('ru'):
        CURRENT_LANG = 'ru'
    elif lang_env.startswith('uz'):
        CURRENT_LANG = 'uz'
    else:
        CURRENT_LANG = 'en'

def _t(key: str, **kwargs) -> str:
    template = TRANSLATIONS.get(CURRENT_LANG, TRANSLATIONS['en']).get(key, TRANSLATIONS['en'].get(key, key))
    if kwargs:
        return template.format(**kwargs)
    return template
