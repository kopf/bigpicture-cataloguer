from distutils.core import setup

import py2exe


py2exe_options = {
    'py2exe': {
        'bundle_files': 1,
        'compressed': True,
        'dll_excludes': 'w9xpopen.exe'
    }
}


setup(console=['bpc/bigpicture.py'], zipfile=None,
      options=py2exe_options)
