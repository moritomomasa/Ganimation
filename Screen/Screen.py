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

# 背景画像のパス
output_bg_path = '../images/bg.png'

# DataBaseのインスタンス化
DB = DataBase()

#ビデオ画面のupdateオンオフ
playing_video = False

# チュートリアル画面
class TutorialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_video(self):
        global playing_video
        playing_video = True
        sm.add_widget(VideoScreen(name='video'))
        print('start')


# 画像設定画面
class SettingsScreen(Screen):
    drop_area_image = ObjectProperty()
    drop_area_label = ObjectProperty()
    image_src = StringProperty('')

    def __init__(self, **kw):
        super(SettingsScreen, self).__init__(**kw)
        Window.bind(on_dropfile=self._on_file_drop)
        # Window.bind(on_cursor_enter=self.on_cursor_enter)
        self.image_src = '../images/faceset.png' #デフォルト画像

    # 画像を読み込む
    def _on_file_drop(self, widndow, file_path):

        if sm.current == "settings":
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


    def start_video(self):
        global playing_video
        playing_video = True
        sm.add_widget(VideoScreen(name='video'))
        print('start')



# 詳細設定画面
class OtherSettingsScreen(Screen):
    drop_area_image = ObjectProperty()
    drop_area_label = ObjectProperty()
    image_src = StringProperty('')

    def __init__(self, **kw):
        super(OtherSettingsScreen, self).__init__(**kw)
        Window.bind(on_dropfile=self._on_file_drop)
        self.image_src = '../images/room.jpg'  # デフォルト画像
        img = cv2.imread(self.image_src, cv2.IMREAD_COLOR)
        cv2.imwrite(output_bg_path, img)

    # 画像を読み込む
    def _on_file_drop(self, widndow, file_path):

        if sm.current == "other_settings":
            print('dropped bg image')

            input_bg_path = str(pathlib.Path(str(file_path, 'utf-8').lstrip("b")))
            root, ext = os.path.splitext(input_bg_path)

            if ext == '.png' or ext == '.jpg' or ext == '.jpeg':
                print('loading dropped bg image')

                img = cv2.imread(input_bg_path, cv2.IMREAD_COLOR)
                cv2.imwrite(output_bg_path, img)

                self.drop_area_label.text = ''
                self.drop_area_image.source = output_bg_path
                self.drop_area_image.reload()

            else:
                self.drop_area_label.text = '画像の読み込みに失敗しました'
                print('->fail')

            return

    def start_video(self):
        global playing_video
        playing_video = True
        sm.add_widget(VideoScreen(name='video'))
        print('start')

# ビデオ画面
class VideoScreen(Screen):
    bg = ObjectProperty()
    anime = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 0.01)
        self.bg.reload()
        print('init video')

    def stop_video(self):
        global playing_video
        playing_video = False
        #self.capture.release()
        sm.remove_widget(self)
        print('stop video')
        print(self.capture)

    def update(self, dt):
        global playing_video
        if playing_video == True:
            ret, self.frame = self.capture.read()
            print(ret)

            # リアル顔画像をデータベースにセット
            #DB.SetRealFaces(self.frame)

            #アニメ顔画像のデータベースから取得
            #self.animeface = DB.GetAnimeFaces()

            # ビデオ表示テスト
            #self.animeface = self.frame
            self.animeface = cv2.resize(self.frame, (280, 280))

            # Kivy Textureに変換
            buf = cv2.flip(self.animeface, -1).tostring()
            texture = Texture.create(size=(self.animeface.shape[1], self.animeface.shape[0]), colorfmt='bgra')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # インスタンスのtextureを変更
            self.anime.texture = texture


'''
class VideoManager(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(1)
        Clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        global playing_video
        if playing_video == True:
            ret, self.frame = self.capture.read()

            # リアル顔画像をデータベースにセット
            DB.SetRealFaces(self.frame)

            #アニメ顔画像のデータベースから取得
            #self.animeface = DB.GetAnimeFaces()

            # ビデオ表示テスト
            self.animeface = self.frame
            self.animeface = cv2.resize(self.frame, (280, 280))

            # Kivy Textureに変換
            buf = cv2.flip(self.animeface, -1).tostring()
            texture = Texture.create(size=(self.animeface.shape[1], self.animeface.shape[0]), colorfmt='bgra')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # インスタンスのtextureを変更
            self.texture = texture
'''

sm = ScreenManager(transition=WipeTransition())
sm.add_widget(TutorialScreen(name='tutorial'))
sm.add_widget(SettingsScreen(name='settings'))
#sm.add_widget(VideoScreen(name='video'))
sm.add_widget(OtherSettingsScreen(name='other_settings'))

class GanimationApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    GanimationApp().run()
