import pathlib
import imghdr
from anime_face_landmark.AnimeFaceDetect import anime_face_detect
from database.DataBase import DataBase
import cv2
import os.path
import numpy as np
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.uix.screenmanager import (ScreenManager, Screen, NoTransition, SlideTransition, CardTransition,
                                    SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition)
#for pupup
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

# 日本語フォント表示対応
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

# フォント読み込み
resource_add_path('./Font')
LabelBase.register(DEFAULT_FONT, 'ipaexg.ttf')

# フォント読み込み Windows用
#resource_add_path('{}\\{}'.format(os.environ['SYSTEMROOT'], 'Fonts'))
#LabelBase.register(DEFAULT_FONT, 'MSGOTHIC.ttc')

# Kivyファイルの読み込み
Builder.load_file('TutorialScreen.kv')
Builder.load_file('SettingsScreen.kv')
Builder.load_file('VideoScreen.kv')
Builder.load_file('OtherSettingsScreen.kv')

# アニメ顔画像のパス
output_path = '../images/output.png'
null_path = '../images/faceset.png'  # 画像未入力時に表示する
selected_face = 1

# 背景画像のパス
output_bg_path = "../images/save/bg/save1/bg.png"
selected_bg = 1

# DataBaseのインスタンス化
DB = DataBase()

#ビデオ画面のupdateオンオフ
playing_video = False
selected_window = "video"

# チュートリアル画面
class TutorialScreen(BoxLayout):
    popup_close = ObjectProperty(None)

# 顔イラスト設定画面
class SettingsScreen(BoxLayout):
    popup_close = ObjectProperty(None)
    to_settings2 = ObjectProperty(None)

    drop_area_image = ObjectProperty()
    drop_area_label = ObjectProperty()
    image_src = StringProperty('')

    def __init__(self, **kw):
        super(SettingsScreen, self).__init__(**kw)
        Window.bind(on_dropfile=self._on_file_drop)
        #Window.bind(on_cursor_enter=self.on_cursor_enter)
        self.image_src = '../images/faceset.png' #デフォルト画像

    # 画像を読み込む
    def _on_file_drop(self, widndow, file_path):
        global selected_window
        if selected_window == "settings":
            print('dropped image')

            input_path = str(pathlib.Path(str(file_path, 'utf-8').lstrip("b")))
            root, ext = os.path.splitext(input_path)

            if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
                print('loading dropped image')

                img = cv2.imread(input_path, cv2.IMREAD_COLOR)

                # external file function
                if anime_face_detect(img):
                    self.drop_area_label.text = ''
                    self.drop_area_image.source = output_path
                    self.drop_area_image.reload()
                    DB.SetSettingImage(output_path)
                else:
                    self.drop_area_label.text = '顔が検出されませんでした'
                    self.drop_area_image.source = null_path
                    self.drop_area_image.reload()
            else:
                self.drop_area_label.text = '画像の読み込みに失敗しました'
                print('->fail')

            return

    def select_button(self, num):
        global output_bg_path
        print(num)
        selectFolder = "../images/save/face/save"+str(num)+"/"
        if not os.listdir(selectFolder):
            print("empty")
        else:
            print("not empty")

# 背景設定画面
class OtherSettingsScreen(BoxLayout):
    popup_close = ObjectProperty(None)
    to_settings1 = ObjectProperty(None)

    drop_area_image = ObjectProperty()
    drop_area_label = ObjectProperty()
    save1 = ObjectProperty()
    save2 = ObjectProperty()
    save3 = ObjectProperty()
    save4 = ObjectProperty()
    save5 = ObjectProperty()
    save6 = ObjectProperty()

    save1_src = StringProperty('')
    save2_src = StringProperty('')
    save3_src = StringProperty('')
    save4_src = StringProperty('')
    save5_src = StringProperty('')
    save6_src = StringProperty('')
    image_src = StringProperty('')

    def __init__(self, **kw):
        super(OtherSettingsScreen, self).__init__(**kw)
        Window.bind(on_dropfile=self._on_file_drop)
        self.image_src = output_bg_path
        self.drop_area_label.text = 'ファイルをドラッグ＆ドロップ'
        self.save1_src = "../images/save/bg/save1/bg.png"
        self.save2_src = "../images/save/bg/save2/bg.png"
        self.save3_src = "../images/save/bg/save3/bg.png"
        self.save4_src = "../images/save/bg/save4/bg.png"
        self.save5_src = "../images/save/bg/save5/bg.png"
        self.save6_src = "../images/save/bg/save6/bg.png"

    # 画像を読み込む
    def _on_file_drop(self, widndow, file_path):
        global selected_window
        if selected_window == "other_settings":
            print('dropped bg image')

            input_bg_path = str(pathlib.Path(str(file_path, 'utf-8').lstrip("b")))
            root, ext = os.path.splitext(input_bg_path)

            if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
                print('loading dropped bg image')

                img = cv2.imread(input_bg_path, cv2.IMREAD_COLOR)
                cv2.imwrite(output_bg_path, img)

                self.drop_area_label.text = ''
                self.drop_area_image.source = output_bg_path
                self.reload_images()

            else:
                self.drop_area_label.text = '画像の読み込みに失敗しました'
                print('->fail')

            return

    def select_button(self, num):
        global output_bg_path
        selectFolder = "../images/save/bg/save"+str(num)+"/"
        if not os.listdir(selectFolder):
            output_bg_path = '../images/bg_null.png'
            self.image_src = '../images/bg_null.png'
            self.drop_area_image.reload()
            print("empty")
        else:
            print("not empty")
            output_bg_path = selectFolder + "bg.png"
            self.image_src = selectFolder + "bg.png"
            self.drop_area_image.reload()
            print(num)

    def reload_images(self):
        self.drop_area_image.reload()
        self.save1.reload()
        self.save2.reload()
        self.save3.reload()
        self.save4.reload()
        self.save5.reload()
        self.save6.reload()

# ビデオ画面
class VideoScreen(Screen):
    bg = ObjectProperty()
    anime = ObjectProperty()
    bg_src = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_src = "../images/save/bg/save1/bg.png"
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 0.01)
        print('init video')
        global playing_video
        playing_video = True

    def stop_video(self):
        global playing_video
        playing_video = False
        self.capture.release()
        print('stop video')

    def start_video(self):
        global playing_video
        playing_video = True
        self.capture.release()
        print('start video')

    def update(self, dt):

        if playing_video == True:
            print("video now")
            ret, self.frame = self.capture.read()
            print(ret)

            # リアル顔画像をデータベースにセット
            DB.SetRealFaces(self.frame)

            #アニメ顔画像のデータベースから取得
            self.animeface = DB.GetAnimeFaces()

            # デバッグ用
            #self.animeface = self.frame
            #self.animeface = cv2.resize(self.frame, (280, 280))

            # Kivy Textureに変換
            buf = cv2.flip(self.animeface, -1).tostring()
            texture = Texture.create(size=(self.animeface.shape[1], self.animeface.shape[0]), colorfmt='bgra')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # インスタンスのtextureを変更
            self.anime.texture = texture

    # チュートリアルポップアップ表示
    def tutorial_popup_open(self):
        self.stop_video()

        content = TutorialScreen(popup_close=self.popup_close)
        self.popup = Popup(title='',separator_height=0, content=content, size_hint=(0.7, 0.7), auto_dismiss=False)
        self.popup.open()

    # 設定ポップアップ表示
    def settings_popup_open(self):
        global selected_window
        selected_window = "settings"
        self.stop_video()

        content = SettingsScreen(popup_close=self.popup_close, to_settings2=self.to_settings2)
        self.popup = Popup(title='',separator_height=0, content=content, size_hint=(0.7, 0.7), auto_dismiss=False)
        self.popup.open()

    # 顔イラスト設定へ画面遷移
    def to_settings1(self):
        global selected_window
        selected_window = "settings"

        self.popup.dismiss()
        content = SettingsScreen(popup_close=self.popup_close, to_settings2=self.to_settings2)
        self.popup = Popup(title='',separator_height=0, content=content, size_hint=(0.7, 0.7), auto_dismiss=False)
        self.popup.open()

    # 背景設定へ画面遷移
    def to_settings2(self):
        global selected_window
        selected_window = "other_settings"

        self.popup.dismiss()
        content = OtherSettingsScreen(popup_close=self.popup_close, to_settings1=self.to_settings1)
        self.popup = Popup(title='',separator_height=0, content=content, size_hint=(0.7, 0.7), auto_dismiss=False)
        self.popup.open()

    def popup_close(self):
        global selected_window
        selected_window = "video"
        self.bg_src = output_bg_path #背景のパスを指定
        self.start_video()
        self.popup.dismiss()
        self.bg.reload() #背景更新
        self.capture = cv2.VideoCapture(1)


sm = ScreenManager(transition=WipeTransition())
sm.add_widget(VideoScreen(name='video'))

class GanimationApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    GanimationApp().run()
