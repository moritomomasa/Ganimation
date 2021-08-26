# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew, gstreamer
block_cipher = None
from pathlib import Path

from pylibdmtx import pylibdmtx
from pyzbar import pyzbar

screen_path="../Screen/"
MISSING_LIBS = (
Path(r'C:\Windows\System32\nvcuda.dll'),
)

a = Analysis(['..\\Screen\\Screen.py'],
             pathex=[
                 'C:\\Users\\KICU\\Projects\\Ganimation\\Ganimation\\App',"../database","../Animator","../Screen",
                 r"C:\Users\KICU\anaconda3\envs\ganimation\Lib\site-packages\torch\lib"  ,
                 r"C:\Users\KICU\anaconda3\envs\ganimation\Lib\site-packages\torch\lib\caffe2_nvrtc.dll"           
             ],
             binaries=[],
             datas=[
                 (r"C:\Users\KICU\anaconda3\envs\ganimation\Lib\site-packages\torch\lib\caffe2_nvrtc.dll","."),
                 (screen_path+"OtherSettingsScreen.kv", '.'),(screen_path+"SettingsScreen.kv", '.'),
                 (screen_path+"TutorialScreen.kv", '.') ,(screen_path+"VideoScreen.kv", '.') ,(screen_path+'/Font/ipaexg.ttf', '.')],
             hiddenimports=['win32file', 'win32timezone'],
             hookspath=[],
             #hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

a.binaries += TOC([
    (Path(dep._name).name, dep._name, 'BINARY')
    for dep in pylibdmtx.EXTERNAL_DEPENDENCIES + pyzbar.EXTERNAL_DEPENDENCIES
])

a.binaries += TOC([(lib.name, str(lib.resolve()),'BINARY') for lib in MISSING_LIBS])


exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='Ganimation',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,Tree('../Screen'),Tree('../Animator'),Tree('../database'),
               a.binaries,
               a.zipfiles,
               a.datas, 
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins + gstreamer.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Ganimation')
