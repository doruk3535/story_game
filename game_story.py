

# ============================================================
# ENGLISH STORY
# ============================================================

STORY_EN = {}

# ============================================================
# TURKISH STORY (EN ile birebir ID + uzunluk)
# ============================================================

STORY_TR = {
"INTRO_VIDEO": {
    "layout": "single_focus",
    "image": "images/intro_building.png",
    "text": "##",

    "ambience_music": "sounds/rain_loop.mp3",
    "ambience_music_volume": 0.6,
    "ambience_loop": True,

    "scene_sequence_cfg": {
        "images": [
            "images/intro_building.png",
        ],
        "holds_ms": [2000],

        "fade_in_ms": 600,
        "fade_out_ms": 600,
        "fade_steps": 64,
        "cover": True,

        "overlay_text": (
            "Burda herşey hep aynı zamanda başlar□||"
            "Ve her seferinde□||"
            "Bir şeyler ters gider.□|||"
        ),

        "overlay_type_ms": 55,
        "overlay_seg_pause_ms": 260,
        "overlay_page_pause_ms": 700,
        "overlay_box_pause_ms": 600,

        "next_scene": "S01_START",
    },
},
"S01_START": {
    "text": (
        "##Saat 02:17||"
        "##Telefon ekranın açık ama bildirim yok||"
        "##⊕Koridordan ayak sesleri geliyor[[BLINK]]||"
    ),
    "images": [
        "images/s01_1_phone.png",
        "images/s01_2.png",
        "images/s01_3.png",
    ],
    "inline_symbol_sfx": {
        "⊕": {"path": "sounds/footstep_loop.mp3", "volume": 1}

    },
    "choices": {
        "1": ("Kapıya Yaklaş", "S02_CORRIDOR_ENTRY", []),
        "2": ("Telefonuna Bak", "S03_PHONE_LOCK", []),
        "3": ("Uyumaya Çalış", "END_E01", []),
    },
},

"S02_CORRIDOR_ENTRY": {
    "text": (
        "##Kapının önündesin□||"
        "Ayak sesleri duruyor||"
        "##Sanki biri seni dinliyor⊕||"
        "##Nefesini duyabiliyorsun."
    ),

    "images": [
        "images/s02_door.png",
        "images/s02_2.png",
        "images/s02_3.png",
    ],

    "inline_symbol_sfx": {
        "⊕": "sounds/breathing.mp3"
    },

    "choices": {
        "1": ("Kapıyı Aç", "S04_CORRIDOR", []),
        "2": ("Kapıyı Kilitle", "S09_LOOP_ROOM", []),
        "3": ("Kapının Altına Bak", "S05_FOOTPRINT", []),
    },
},
"S03_PHONE_LOCK": {
    "text": (
    "##Kilit ekranına bakıyorsun||"
    "##⊕Eski bir bildirim var||"
    "##Bugüne ait değil||"
    "Gönderen bilinmiyor.[[BLINK]]||"
),
    "inline_symbol_sfx": {
        "⊕": "sounds/notification.mp3"
    },
    "images": [
        "images/s03_phone.png",
        "images/s03_2.png",
        "images/s03_3.png",
    ],
    "choices": {
        "1": ("Bildirimi aç", "S03_5_NOTIFICATION", ["O2"]),
        "2": ("Telefonu kapat", "S09_LOOP_ROOM", []),
        "3": ("Galeriyi aç", "S06_GALLERY", []),
    },
},

"S03_5_NOTIFICATION": {
    "text": (
    "##Kurtul oradan□||"
    "Çabuk□||"
    "Orası artık güvenli değil□||"
    "Sakın kimseye güvenme[[BLINK]]||"
),
"layout": "single_focus",
    "images": [

        "images/s03_5_notification.png",

    ],
    "choices": {
        "1": ("Koridora çık", "S04_CORRIDOR_After_NOTIFICATION", ["O2"]),
        "2": ("Telefonu kapat", "S09_LOOP_ROOM", []),
        "3": ("Galeriyi aç", "S06_GALLERY", []),
    },
},


    "S04_CORRIDOR": {
        "text": (
    "⊕##Koridor sessiz□||"
    "Işıklar hafifçe titriyor□||"
    "İleride biri var.[[BLINK]]"
    
),
    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    },"layout": "single",
        "images": ["images/s04_corridor.png"],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
        },
    },
"S04_CORRIDOR7": {
   "text": (
    "⊕##Tekrar koridordasın□||"
    "Bomboş□||"
    "Az önce biri vardı□||"
    "Ama artık yok.□[[BLINK]]"
),
    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    },"layout": "single",
        "images": ["images/s04_corridor_empty.png"],
        "choices": {
            "1": ("Yangın merdivenine git", "S15_FIRE_EXIT", []),
            "2": ("Yemekhaneye yönel", "S16_CAFETERIA_FROM_CAMERA", []),
            "3": ("Odana geri dön", "S09_LOOP_ROOM_4", []),
        },
    },
    "S04_CORRIDOR_After_NOTIFICATION": {
        "text": (
    "⊕##Koridor sessiz□||"
    "Işıklar hafifçe titriyor□||"
    "İleride biri var.[[BLINK]]"
),
    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    }, "layout": "single",
        "images": [ "images/s04_corridor.png"],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_1", []),
        },
    },
    "S04_CORRIDOR_after_footprint": {
        "text": (
    "⊕##Ayak izleri ileri uzanıyor□||"
    "Koridor sessiz□||"
    "Işıklar hafifçe titriyor□||"
    "İlerde biri var.[[BLINK]]"
),
    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    },"layout": "single",
        "images": ["images/s04_corridor.png"],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },

    "S04_CORRIDOR_AFTER_GALERY": {
        "text": (
    "⊕##Bir saniye□||"
    "Bu koridoru tanıyorum□||"
    "Daha önce gördüğüme emininm□||"
    "Neden hatırlayamıyorum.□[[BLINK]]"
),    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    },"layout": "single",
        "images": [ "images/s04_corridor.png"],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki adama sor", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },

    "S04_CORRIDOR_After_camera": {
        "text": (
    "⊕##Tekrar koridordasın□||"
    "Bomboş□||"
    "Az önce biri vardı□||"
    "Ama artık yok.[[BLINK]]"
),    "inline_symbol_sfx": {
        "⊕": "sounds/flicker.mp3"
    },"layout": "single",
        "images": [ "images/s04_corridor_empty.png"],
        "choices": {
            "1": ("Yangın merdivenine git", "S15_FIRE_EXIT", []),
            "2": ("Yemekhaneye yönel", "S16_CAFETERIA_FROM_CAMERA", []),
            "3": ("Odana geri dön", "S09_LOOP_ROOM_4", []),
        },
    },
"S16_CAFETERIA_FROM_FIGHT": {
    "layout": "single",
    "text": (
    "Yemekhaneye doğru yürüyorsun□||"
    "⊕Kapıyı açıyorsun□||"
    "İçerisi… fazla aydınlık.[[BLINK]]□|||"

    "##Ve girer girmez birini görüyorsun□||"
    "Sende kimsin ???||"
    "Nedenini nasılını soramadan.[[BLINK]]□|||"

    "‘Acele et, burdan kurtulmamız gerek.’ diyor□||"
    "‘Bize bi anahtar lazım… yangın çıkışı için.[[BLINK]]’"
),
   "inline_symbol_sfx": {
        "⊕": "sounds/door_opening.mp3"
    },

    "image": "images/s16_cafeteria_from_camera.png",
    "choices": {
        "1": ("Saklan", "S16_CAFETERIA_HIDE", []),
        "2": ("Birlikte hareket et", "S16_CAFETERIA_CHECK_AROUND", []),
        "3": ("Tek başına hareket et", "S16_CAFETERIA_SOLO", []),
    },
},
"S16_CAFETERIA_FROM_CAMERA": {
    "layout": "single",
    "text": (
    "Yemekhaneye doğru yürüyorsun□||"
    "⊕Kapıyı açıyorsun□||"
    "İçerisi… fazla aydınlık.[[BLINK]]□|||"

    "##Ve girer girmez birini görüyorsun□||"
    "Bu sensin,kameralarda gördüğün kişi□||"
    "Nedenini nasılını soramadan.[[BLINK]]□|||"

    "‘Acele et, burdan kurtulmamız gerek.’ diyor□||"
    "‘Bize bi anahtar lazım… yangın çıkışı için.□[[BLINK]]’"
),   "inline_symbol_sfx": {
        "⊕": "sounds/door_opening.mp3"
    },

    "image": "images/s16_cafeteria_from_camera.png",
    "choices": {
        "1": ("Saklan", "S16_CAFETERIA_HIDE", []),
        "2": ("Birlikte hareket et", "S16_CAFETERIA_CHECK_AROUND", []),
        "3": ("Tek başına hareket et", "S16_CAFETERIA_SOLO", []),
    },
},

"S16_CAFETERIA_CHECK_AROUND": {
    "layout": "single",
    "text": (
    "##Çabuk□||"
    "Benimle gel.[[BLINK]]"
),
    "image": "images/s16_cafeteria_check_around2.png",
    "choices": {
        "1": ("Tezgâha yönel", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        "2": ("Saklan", "S16_CAFETERIA_HIDE_DUO", []),
        "3": ("Kapıya kulak ver", "S16_CAFETERIA_LISTEN_DUO", []),
    },
},

 
"S16_CAFETERIA_CHECK_AROUND2": {
    "layout": "single",
    "text": (
    "##Çabuk||"
    "Benimle gel.[[BLINK]]"
),
    "image": "images/s16_cafeteria_check_around2.png",
    "choices": {
        "1": ("Tezgâha doğru yönelin", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        "2": ("Saklanın", "S16_CAFETERIA_HIDE_DUO", []),
    },
},




"S16_CAFETERIA_CHESS_SETUP_DUO": {

    "text": (
    "##Tezgâhın arkasına geçiyorsunuz□||"
    "Burası çalışanlara ait gibi duruyor□||"
    "Birsürü çekemece var□||"
    "Ama biri denense şifreyle kilitlenmiş.[[BLINK]]□|||"
    "Çekmeceyi zorluyorsun ama açılmıyor.□||"
    "Etrafı incelediğinde iki şey görüyorsun||"
    "##Bir satranç tahtası.[[BLINK]]□|||"
    "##Ve bir yangın tüpü□||"
    "Ne yapmalıyım?[[BLINK]]"
),
    "images": [
        "images/s16_1_counter_back_copy.png",     # sol: tezgâh arkası / çekmeceler
        "images/s16_2_locked_drawer_copy.png",    # orta: satranç tahtası
        "images/s16_3_chess_and_extinguisher_copy.png",        # sağ: yangın tüpü / kilit
    ],
    "choices": {
        "1": ("Satranç tahtasını incele", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın tüpüyle \n kilidi kırmaya çalış", "S16_yangın_tüpü_duo", []),
        "3": ("Yakalanmadan saklan", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_CHESS_PUZZLE_SCREEN_DUO": {
    "layout": "single",
    "images": ["images/s16_chess_puzzle_screen_copy.png"],
    "text": (
    "##Tahtaya bakıyorsun||"
    "Taşlar sana bir şey ima ediyor gibi||"
    "Oyun sonu çok yakın||"
    "Taşların koordinatları sana bir şeyler anlatıyor.[[BLINK]]□|||"
    "Şifre bu olabilir mi?||"
    "Ama hangi taş ve hangi koordinat?[[BLINK]]□|||"
    "Biraz düşündükten sonra fark ediyorsun:||"
    "BULDUM! Tek hamlede mat var||"
    "ŞİFRE BU OLMALI.[[BLINK]]"
),
    "choices": {
        "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A_DUO", []),
        "2": ("At g6'ya oynar", "S16_CHESS_TRY_B_DUO", []),
        "3": ("At f7'ye oynar", "S16_CHESS_TRY_C_DUO", []),
    },
},




"S17_DUO_ESCAPE_RUN": {
    "text": (
    "##Anahtarı avucunda sıkıyorsun||"
    "Gelecekteki halin yanında||"
    "-Şimdi.[[BLINK]]□|||"
    "⊕İkiniz birden koridora fırlıyorsunuz||"
    "Ayak sesleriniz bütün koridorda yankılanıyor.[[BLINK]]□|||"
    "Koridor boyunca koştuktan sonra||"
    "##Yangın çıkışına geliyorsunuz.[[BLINK]]□|||"
    "Kapıya vardığında anahtarı kilide sokuyorsun||"
    "##Bekleyin herşeyi mahvediceksiniz||"
    "✦Tık.[[BLINK]]□|||"
    "Kapı açılıyor ve—.[[BLINK]]□|||"
    "Bu bir çıkış kapısı değil.[[BLINK]]□|||"
), "inline_symbol_sfx": {
    "⊕": {"path": "sounds/run.mp3", "volume": 1},
    "✦": {"path": "sounds/door_lock.mp3", "volume":1}
},
    "images": [
        "images/s17_duo_escape_1_run_corridor.png",
        "images/scene_fire_exit_door.png",
        "images/s17_duo_escape_3_janitor_reveal.png",
    ],
    "auto_next": "S17_DUO_PORTAL_OPENS",
    "auto_next_after": True,
    "auto_next_delay_ms": 250,
},

"S17_DUO_PORTAL_OPENS": {
    # ✅ fallback görsel: gerçekten var olan bir PNG olmalı
    # sende bg.png var görünüyor, istersen onu koy:
    "image": "images/image_copy.png",

    # ✅ MP4 oynat
    "video": {
        "path": "images/portal_anim/portal.mp4",
        "fps": 24,
        "loop": True
    },
    "inline_symbol_sfx": {
        "⊕": {"path": "sounds/portal.mp3", "volume": 0.65}
    },
    "text": (
    "⊕##Bu bir zaman portalı||"
    "İçinden geçip giden zamanı hissedebiliyorsun||"
    "Aynı anın kırık parçaları||"
    "Uğultu yükseliyor||"
),

    "auto_next": "S17_DUO_TALK_WITH_JANITOR",
    "auto_next_after": True,
    "auto_next_delay_ms": 350,
},
"S17_DUO_TALK_WITH_JANITOR": {
    "layout": "single",
    "image": "images/s17_duo_talk_with_janitor.png",

    "text": (
    "##Bekleyin herşeyi anlatıcam :||"
    "\"Sizin burda olmanız tamamıyla benim suçum\"||"
    "\"Uzun zaman önceydi\"||"
    "\"Yada değildi||"
    "\"Tam hatırlayamıyorum |||"
    "\\Zamanla çok oyanmanında sorunu bu.[[BLINK]]\"□||"
    "\"Başlarsan asla duramazsın.[[BLINK]]\"□||"
    "\"Zaten yeterince karıştı.[[BLINK]]\"□|||"
    "\"Burdan çıkmaya çalışarak||"
    "\\Milyarlarca hayatı riske attığınız görmüyormusunuz.[[BLINK]]\"□|||"
    "\"Bir seçim yapmak zorundayız.[[BLINK]]\"□|||"
    "\"Sen bir anomalisin ve burda kalmak zorundasın||"
    "\"Belki seni burda tutmaya artık gücüm yetmez||"
    "\"Ama yaptıklarınının sonuçlarını olduğnunu unutma||"
),

    "choices": {
        "1": ("Ortanca halinle kaç", "END_DUO_ESCAPE_TWO_LEAVE", []),
        "2": ("Ortanca halini gönder, sen kal", "END_DUO_STAY_SOLO_SACRIFICE", []),
        "3": ("Hepimiz beraber kaçalım", "END_DUO_ESCAPE_ALL_THREE", []),
    },
},
"END_DUO_ESCAPE_ALL_THREE": {
    "text": (
    "##Ozaman bizimle gel.[[BLINK]]□|||"
    "Zamanı bizden daha biliyosun||"
    "Sana ihtiyacımız var.[[BLINK]]□|||"
    "Hayatın boyunca burda tutsak yaşıyamazsın□||"
    "-Bu riski alamam□||"
    "Biz burdan gidiyoruz.[[BLINK]]□|||"
    "SENLE YADA SENSİZ.[[BLINK]]□|||"
    "##Portaldan geçiyorsunuz||"
    "AHHH||"
    "Gerçekten ne kadarda inatçıyım||"
    "##Benide bekleyin||"
),
    "images": [
        "images/end_duo_two_leave_4_dash_into_portal.png",
        "images/end_duo_two_leave_2_time_layers_flash.png",
        "images/end_attack_portal_jump_3_follow.png",
    ],

    # ✅ MÜZİK EN BAŞTAN
    "scene_music": "sounds/ending_theme6.mp3",
    "scene_music_volume": 0.30,
    "auto_next": "END_ATTACK_WHITE_ROOM",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
    "ending_id": "END_ATTACK_PORTAL_JUMP",
},
"END_DUO_ESCAPE_TWO_LEAVE": {
    "text": (
    "##Gelecekteki halinin bileğini yakalıyorsun.□||"
    "-Koş.[[BLINK]]□|||"
    "Bir an tereddüt ediyor□||"
    "Sonra gözlerini kısıyor□||"
    "Hadi yapalım □||"
    "##İkiniz birden portala hamle ediyorsunuz.[[BLINK]]□|||"
    "Hademe arkanızdan bağırıyor:□||"
    "-Durun!||"
    "Söylediklerimden hiç mi bir şey anlamadınız□||"
    "Bütün varoluşu yok edeceksiniz□.[[BLINK]]□|||"
    "##Ama artık duymuyorsunuz bile.□||"
    "Portalın içi sizi yutuyor||"
),

    "images": [
        "images/end_duo_two_leave_1_dash_into_portal.png",
        "images/end_duo_two_leave_2_time_layers_flash.png",
        "images/end_duo_two_leave_3_bed_0218.png",
    ],

    "scene_music": "sounds/ending_theme4.mp3",
    "scene_music_volume": 0.20,

    "auto_next": "S18_DUO_WAKEUP_0218",
    "auto_next_after": True,
    "auto_next_delay_ms": 350,
},
# 2) Uyanma sahnesi (seçenek: sadece koridora çık)
"S18_DUO_WAKEUP_0218": {
    "text": (
    "##Gözlerin zorla açılıyor□||"
    "##Oda tanıdık…||"
    "##Karşında biri var□||"
    "Sen.□||"
    "Çabuk, benimle gel□.[[BLINK]]□|||"
    "-Ne oldu?||"
    "Soru sorma, çabuk||"
),
    "images": [
        "images/end_ending_1.png",
        "images/s18_wakeup_2_middle_close.png",
        "images/s18_wakeup_3_reach_door.png",
    ],
    "auto_next": "S18_DUO_SEE_RIFT",
    "auto_next_after": True,
    "auto_next_delay_ms": 500,
},

"S18_DUO_SEE_RIFT": {
    "layout": "single_focus",
    "image": "images/s18_rift_2_giant_time_rift.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_DUO_RIFT_OUTSIDE",

    "ending_sequence_cfg": {
        "images": [
            "images/s18_rift_2_giant_time_rift.png",
        ],
        "holds_ms": [3000],

        "instant_switch": False,
        "fade_in_ms": 1000,
        "fade_out_ms": 1000,
        "fade_steps": 64,
        "cover": True,

        "overlay_text": (
    "Zaman çoktan yok olmaya başlamış.□||"
    "Biz ne yaptık.□||"
    "-Bunu biz yapmadık.[[BLINK]]□|||"
),

        "overlay_type_ms": 55,
        "overlay_seg_pause_ms": 260,
        "overlay_page_pause_ms": 600,
        "overlay_box_pause_ms": 600,

        "next_scene": "LOBBY",
    },

    "final_screen_line": "Ama biz düzelteceğiz.",
    "ending_title": "Zamansız Son",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,
},

"END_DUO_STAY_SOLO_SACRIFICE": {
    "text": (
    "Gelcekteki haline bakıyorsun||"
    "Git.[[BLINK]]□|||"
    "-Ne?||"
    "Birinin burda kalması||"
    "Ve Zamanın bütünlüğünü koruması gerek||"
    "Eğer biri kalacaksa… o ben olmalıyım\"||"
    "Anahtarı onun avucuna itiyorsun.[[BLINK]]□|||"
    "Gitmek zorundasın||"
    "Hademe sessizce izliyor||"
    "Böyle olmak zorunda||"
    "Son bir kez sana bakıyor.[[BLINK]]□|||"
    "Ve portaldan yavaşca geçiyor||"
    "Hademe ağır ağır yaklaşıyor||"
    "Aferin evlat||"
    "Doğru olanı yaptın||"
),
    "auto_next": "END_SOLO_STAY_PROTECT_TIME_A",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},


"S16_DUO_CHECK_SOUND": {
    "images": [
        "images/s16_duo_check_sound_left.png",    # 0 sol
        "images/s16_duo_check_sound.png",         # 1 orta (ikinci görsel)
        "images/s16_duo_check_sound_right.png",   # 2 sağ
    ],

    # Orta panele flicker
    "flicker": {"index": 1, "slot": "B", "intensity": "strong", "until": "scene_end"},

    "text": (
    "##Sesin geldiği kapıya yaklaşıyorsun||"
    "Gelecekteki halin hemen arkanda||"
    "Tıkırtı bir anda kesiliyor.[[BLINK]]□|||"
    "##Kafeteryadaki ışıklar bir an… yanıp sönmeye başlıyor||"
    "##İkiniz de aynı anda arkanızı dönüyorsunuz.[[BLINK]]□|||"
    "Koridorun ucunda bir gölge||"
    "Hademe.[[BLINK]]□|||"
    "Bu sefer koşmuyor||"
    "Sakin bir şekilde üzerinize geliyor.[[BLINK]]□|||"
    "[[BLACK2000.[[BLINK]]]]"
),
"auto_next": "S15_CAFETERIA_STORAGE_DUO",
"auto_next_after": True,
"auto_next_delay_ms": 0,
    
},



"S16_CHESS_TRY_A_DUO": {
    "layout": "single",
    "images": [ "images/s16_chess_try_a_copy.png"],
    "text": (
    "##Kale h7 gibi ama emin değilim ||"
    "Ozaman şifre h7 olabilirmi||"
    "Denemekten zarar gelmez herhalde||"
),
    "choices": {
        "1": ("Şifreyi deneyelim bakalım", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü_duo", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_yangın_tüpü": {
    "layout": "single",
    "image": "images/s16_yangin_tupu_duo.png",

    "text": (
    "Tezgahın üstündeki yangın tüpünü alıp.□||"
    "⊕##Kilide doğru ⊕vuruyorsun.□||"
    "⊕Tok birkaç darbede işi hallediyorsun.[[BLINK]]□|||"
    "Kilidi kırdın.□||"
    "Ama Ses tüm kafeteryada yankılandı.[[BLINK]]□|||"
    "Ayak sesleri||"
    "Üzerine doğru geliyor||"
),    "inline_symbol_sfx": {
        "⊕": {"path": "sounds/metal_hit.mp3", "volume": 0.65}
    },

    # burada artık “hademe seni gördü” sahnesine geçiyoruz
    "auto_next": "S16_HADEME_SENI_GORDU",
    "auto_next_after": True,

    # istersen minik gerilim gecikmesi:
    "auto_next_delay_ms": 350,
},

"S16_HADEME_SENI_GORDU": {
    "layout": "single",
    "image": "images/s16_hademe_seni_gordu_duo.png",

    "text": (
    "##Arkanı dönüyorsun—□||"
    "Hademe.□||"
    "Yüzü ifadesiz.[[BLINK]]□|||"
    "Seni tek hamlede elinden tutun sürüklüyor||"
    "⊕Kapı açılıyor.[[BLINK]]□|||"
    "Karanlık bir depo.□||"
    "İçeri itiliyorsun.□.[[BLINK]]□|||"
    "✦Kapı arkandan kapanıyor||"
    "Kilit sesi…□||"
),"inline_symbol_sfx": {
    "⊕": {"path": "sounds/door_open.mp3", "volume": 0.65},
    "✦": {"path": "sounds/door_closing.mp3", "volume": 0.65}
},

    # mevcut sahneye aynı şekilde bağlanıyor
    "auto_next": "S15_CAFETERIA_STORAGE",
    "auto_next_after": True,

    # burada da çok kısa bir “şok” gecikmesi hoş durur:
    "auto_next_delay_ms": 0,
},
"S16_yangın_tüpü_duo": {
    "layout": "single",
    "image": "images/s16_yangin_tupu_duo.png",

    "text": (
    "Tezgahın üstündeki yangın tüpünü alıp.□||"
    "⊕##Kilide doğru vuruyorsun.⊕□||"
    "⊕Tok birkaç darbede işi hallediyorsun.[[BLINK]]□|||"

    "Kilidi kırdın.□||"
    "Ama Ses tüm kafeteryada yankılandı.[[BLINK]]□|||"

    "Ayak sesleri||"
    "Üzerine doğru geliyor||"
),
  "inline_symbol_sfx": {
        "⊕": {"path": "sounds/metal_hit.mp3", "volume": 0.65}
    },
    # burada artık “hademe seni gördü” sahnesine geçiyoruz
    "auto_next": "S16_HADEME_SENI_GORDU_DUO",
    "auto_next_after": True,

    # istersen minik gerilim gecikmesi:
    "auto_next_delay_ms": 350,
},

"S16_HADEME_SENI_GORDU_DUO": {
    "layout": "single",
    "image": "images/s16_hademe_seni_gordu_duo.png",

    "text": (
    "##Arkanı dönüyorsun—□||"
    "Hademe.□||"
    "Yüzü ifadesiz.[[BLINK]]□|||"

    "Sizi tek hamlede elinden tutun sürüklüyor||"
    "⊕Kapı açılıyor.[[BLINK]]□|||"

    "Karanlık bir depo.□||"
    "İçeri itiliyorsun.□.[[BLINK]]□|||"

    "✦Kapı arkandan kapanıyor||"
    "Kilit sesi…□||"
),"inline_symbol_sfx": {
    "⊕": {"path": "sounds/door_open.mp3", "volume": 0.65},
    "✦": {"path": "sounds/door_closing.mp3", "volume": 0.65}
},
    # mevcut sahneye aynı şekilde bağlanıyor
    "auto_next": "S15_CAFETERIA_STORAGE_DUO",
    "auto_next_after": True,

    # burada da çok kısa bir “şok” gecikmesi hoş durur:
    "auto_next_delay_ms": 0,
},
"S16_CHESS_TRY_B_DUO": {
    "layout": "single",
    "images": ["images/s16_chess_try_b_copy.png"],
    "text": (
    "##Atı g6'ya oynuyorsun||"
    "Ozaman şifre g6 olabilirmi||"
    "Denemekten zarar gelmez herhalde:||"
),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü_duo", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},

"S16_CHESS_TRY_C_DUO": {
    "layout": "single",
    "images": [ "images/s16_chess_try_c.png"],
    "text": (
    "##Atı f7'ya oynuyorsun||"
    "Ozaman şifre f7 olabilirmi||"
    "Denemekten zarar gelmez herhalde:||"
),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü_duo", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_kilit_açılmıyor_DUO_A": {
    "text": (
    "##Yanlış hesaplamış olmalıyım||"
    "Bidaha denemeliyim||"
),
"layout": "single",
    "images": [ "images/s16_kilit_acilmiyor_duo_a.png"],

    "choices": {
        "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın söndürücüyü al", "S16_şifre_doğru_DUO", []),
        "3": ("SAKLAN !!!", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_kilit_açılmıyor_DUO_C": {
    "text": (
    "##Yanlış hesaplamış olmalıyım||"
    "Bidaha denemeliyim||"
),"layout": "single",
    "images": [ "images/s16_kilit_acilmiyor_duo_c.png"],

    "choices": {
        "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın söndürücüyü al", "S16_şifre_doğru_DUO", []),
        "3": ("SAKLAN !!!", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
   "S16_UNLOCK_SEQUENCE_DUO": {
       "layout": "single",
        "images": [ "images/s16_1_counter_back_copy.png"],
        "text": (
    "##Tezgâhın altına eğiliyorsun||"
    "Şifreli olan kilidi şifreni girmeye hazırlanıyorsun||"
),

        "choices": {
            "1": ("h7 ", "S16_kilit_açılmıyor_DUO_A", []),
            "2": ("g6", "S16_şifre_doğru_DUO", []),
            "3": ("f7", "S16_kilit_açılmıyor_DUO_C", []),
        },
    },

    "S16_CAFETERIA_HIDE_DUO": {
        "text": (
    "##Tezgâhın altına giriyorsunuz||"
    "Dizleriniz buz gibi taş zeminde||"
    "⊕Kapı açılıyor.[[BLINK]]□|||"

    "-Nerdesiniz... orada olduğunuzu biliyorum'||"
    "Size doğru küçük adım sesleri geliyor||"
    "Ayakkabısının sesi... duruyor. Tam önünde.[[BLINK]]"
    
),
"layout": "single",
"images": [ "images/s16_cafeteria_hide.png"],

        "choices": {
            "1": ("Sessiz kal / nefesini tut", "S15_HIDE_SILENT_1_DUO", ["F_HIDE"]),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
            "3": ("Etrafı Aramya başlayın.'", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        },
        "inline_symbol_sfx": {
            "⊕": {"path": "sounds/door_open.mp3", "volume": 0.65}
        },
    },
    # Alias: Akış değişmesin diye S15_FIRE_EXIT'ı kilitli sahneye yönlendiriyoruz
"S15_FIRE_EXIT": {
    "text": (
    "##Yangın kapısının önündesin||"
    "Kolu indiriyorsun||"
    "Kımıldamıyor||"
    "Kilitli||"
),"layout": "single",
    "images": [
        "images/s15_fire_exit.png",
    ],
    "choices": {
        "1": ("Geri dön", "S04_CORRIDOR_After_camera", []),
        "2": ("Odana dön", "S09_LOOP_ROOM_4", []),
        "3": ("Yemekhaneye git", "S16_CAFETERIA_FROM_CAMERA", []),
    },
},


    "S05_FOOTPRINT": {
        "layout": "single",
        "text": (
    "Yerde bir ayakkabı izi||"
    "Nedense çok tanıdık.[[BLINK]]"
),
        "image": "images/s05_footprint.png",
        "choices": {
            "1": ("İzi takip et", "S04_CORRIDOR_after_footprint", []),
            "2": ("Görmezden gel", "S09_LOOP_ROOM_2", []),
            "3": ("Fotoğrafını çek", "S06_GALLERY_after_footprint", []),
        },
    },

    "S06_GALLERY_after_footprint": {
        "text": (
    "⊕##Fotoğrafını çektin||"
    "Ve bakmak için galeriyi açtın||"
    "##Galerinde eski fotoğraflar var||"
    "Çoğunu hatırlamıyorsun.[[BLINK]]□|||"

    "Ama biri öne çıkıyor:||"
    "##Koridor,||"
    "Gece,||"
    "Ve sen||"
), "inline_symbol_sfx": {
        "⊕": {"path": "sounds/photo.mp3", "volume": 0.65}
    },
        "images": [
            "images/s06_gallery.png",
            "images/s06_2.png",
            "images/s06_3.png",
        ],
        "effects": ["SET_FLAG_GALLERY_SEEN"],
        "choices": {
            "1": ("Fotoğrafı incele", "S10_MEMORY_GLITCH", []),
            "2": ("Galeriden çık ve dışarıyı incele", "S04_CORRIDOR_AFTER_GALERY", []),
            "3": ("Fotoğrafı sil", "S09_LOOP_ROOM_2", []),
        },
    },

    "S06_GALLERY": {
        "text": (
    "##Galerinde eski fotoğraflar var||"
    "##Çoğunu hatırlamıyorsun||"
    "Ama biri öne çıkıyor:||"
    "##Koridor,Gece,Ve sen.[[BLINK]]"
),
        "images": [
            "images/s06_gallery.png",
            "images/s06_2.png",
            "images/s06_3.png",
        ],
        "effects": ["SET_FLAG_GALLERY_SEEN"],
        "choices": {
            "1": ("Fotoğrafı incele", "S10_MEMORY_GLITCH", []),
            "2": ("Galeriden çık ve kapının önüne çık", "S04_CORRIDOR_AFTER_GALERY", []),
            "3": ("Fotoğrafı sil", "S09_LOOP_ROOM_2", []),
        },
    },

    "S07_CAMERA_DOOR": {
        "text": (
    "##Kamera odasının kapısındasın||"
    "İçeriden hafif bir uğultu geliyor||"
    "Kapı açık.[[BLINK]]"
),
"layout": "single",
        "images": [ "images/s07_camera_door.png"],
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("içeriyi dinle", "S12_CAMERA_HINT", []),
            "3": ("koridora geri dön", "S04_CORRIDOR_After_camera", []),
        },
    },

    "S08_JANITOR": {
        "text": (
    "##Temizlik arabasının yanında biri duruyor||"
    "##Gece temizlikçisi||"
    "##Seni görünce kaşlarını çatıyor||"
    "Sanki seni tanıyor.[[BLINK]]"
),
        "images": [
            "images/s08_janitor.png",
            "images/s08_2.png",
            "images/s08_3.png",
        ],
        "choices": {
            "1": ("Onunla konuş", "S13_JANITOR_DIALOGUE", ["O3"]),
            "2": ("Sessizce yanından geç", "S08.5_DONT_LOOK_HİM", []),
            "3": ("Odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },

    "S08.5_DONT_LOOK_HİM": {
        "text": (
    "##Sana baktı ve dediki||"
    "Bu saatte koridorda gezmenin||"
    "Yasak olduğunu bilmiyormusun||"
),
"layout": "single",
        "images": [ "images/S08.5_DONT_LOOK_HİM.png"],
        "choices": {
            "1": ("Tersle", "S8.4_ANSWER_HİM", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },

    "S8.4_ANSWER_HİM": {
        "text": (
    "##Sen kendi işine bak||"
    "Bunu pek hoş karşılamayan bi ses tonu ve bakışla||"
    "'Çabuk odana dön' dedi||"
),
"layout": "single",
        "images": [ "images/S08.4_answer_him.png"],
        "choices": {
            "1": ("Haddini bildir", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },

"S8.6_go_to_caffeteria": {
    "text": (
    "##Bir anda koşmaya başlıyorsun||"
    "##Adımların koridorda yankılanıyor||"
    "Işıklar gözünü alıyor||"
    "##Tam önünde duruyor|| "
    "Kafeterya||"
),"inline_symbol_sfx": {
        "⊕": {"path": "sounds/run.mp3", "volume": 0.65}
    },
    "images": [
        "images/s08_6_collision.png",
        "images/s08_6_2.png",
        "images/s08_6_3.png",
    ],

 "choices": {


        "1": ("Kafeteryaya gir", "S8.7_CAFETERIA_KARSILASMA", []),


    },
},
"S8.7_CAFETERIA_KARSILASMA": {
    "text": (
    "##İçerde birine çarpıyorsun||"
    "Çarpmanın etkisiyle yere düşüyo||"
    "##Dur bi saniye sende kimsin.[[BLINK]]□|||"

    "Ve Neden||"
    "##Bana benziyorsun ???||"
),
    "images": [
        "images/s08_7_1.png",
        "images/s08_7_2.png",
        "images/s08_7_3.png",
    ],
    "choices": {
        "1": ("Onu görmezden gel ve saklan", "S16_CAFETERIA_SOLO", []),
        "2": ("Onunla birlikte hareket et", "S16_CAFETERIA_CHECK_AROUND2", []),
        "3": ("Kim olduğunu anlamaya çalış", "END_CAUGHT_WHILE_REALIZING", []),
    },
},


"S16_CAFETERIA_SOLO": {
    "layout": "single_focus",          # ✅ HERO MODE
    "image": "images/s16_cafeteria_solo.png",  # ← BU GÖRSEL (attığın görsel)
    # İstersen boyutu override edebilirsin:
    # "hero_canvas": {"w": 1500, "h": 700},

    "text": (
    "##Tek başına ilerlemeyi kafaya koymuşsun||"
    "Işıklar açık||"
    "Masa ve sandalyeler düzgün.[[BLINK]]□|||"

    "Her şey fazla normal||"
    "⊕Kapıyı arkandan kapatıyorsun||"
    "Kapıyı kapattığın anda ||"
    "Birkaç saniye sonra.[[BLINK]]□|||"
    "Sesler kesiliyor||"
    "Sessizlik geri geliyor||"
    "Bununla unutup yoluna bakman gerek.[[BLINK]]"
),"inline_symbol_sfx": {
        "⊕": {"path": "sounds/door_closing.mp3", "volume": 0.65}
    },
    "choices": {
        "1": ("Tezgâhın arkasına bak", "S16_CAFETERIA_CHESS_SETUP", []),
        "2": ("Saklanacak bir yer ara", "S16_CAFETERIA_HIDE", []),
        "3": ("Sesin geldiği yöne kulak kesil", "S16_CAFETERIA_LISTEN", []),
    },
},
"S15_STORAGE_LISTEN": {
    "layout": "single",
    "image": "images/s15_cafeteria_storage_duo.png",

    "text": (
    "Sessizce oturup bekliyorsunuz||"
    "Yapıcak bişeyiniz yokmuş gibi||"
    "-Peki gelecekt bana bahsedilceğin bişey varmı…[[BLINK]]□|||"
    "Sayısal loto numaraları gibi||"
    "-Gelecek hakkında bilgi veremem||"
    "Hiç mi geleceğe dönüş izlemedin.[[BLINK]]"
),

    "choices": {
        "1": ("Havalandırmayı kullan", "S15_RAY_VENT_ESCAPE_SOLO", []),
        "2": ("Hademeye seslen", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),

    },
},
"S16_CAFETERIA_CHESS_SETUP": {
    "text": (
    "##Tezgâhın arkasına geçiyorsun||"
    "Burası çalışanlara ait gibi duruyor||"
    "Çekmeceler düzenli, ama biri denense şifreyle kilitlenmiş.[[BLINK]]□|||"
    "Çekmeceyi zorluyorsun ama açılmıyor||"
    "Etrafı incelediğinde iki şey görüyorsun ||"
    "##Bir satranç tahtası||"
    "##Ve bir yangın tüpü:||"
),
    "images": [
        "images/s16_1_counter_back.png",
        "images/s16_2_locked_drawer.png",
        "images/s16_3_chess_and_extinguisher.png",
    ],
    "choices": {
        "1": ("Satranç tahtasını incele", "S16_CHESS_PUZZLE_SCREEN", []),
        "2": ("Yangın tüpüyle \n kilidi kırmaya çalış", "S16_yangın_tüpü", []),
        "3": ("Yaşlı adam gelemden saklanıcak biyer bul", "S16_CAFETERIA_HIDE", []),
    },
},
    "S16_CAFETERIA_HIDE": {
        "text": (
    "##Tezgâhın altına giriyorsun||"
    "Dizlerin buz gibi taş zeminde||"
    "⊕Kapı açılıyor.[[BLINK]]□|||"

    "-Nerdesiniz... orada olduğunuzu biliyorum'||"
    "Size doğru küçük adım sesleri geliyor||"
    "Ayakkabısının sesi... duruyor. Tam önünde.[[BLINK]]"
    
),
    "inline_symbol_sfx": {
        "⊕": {"path": "sounds/door_open.mp3", "volume": 0.65}
    },
    "layout": "single",
    "image": "images/s16_cafeteria_hide.png",

        "choices": {
            "1": ("Sessiz kal / nefesini tut", "S15_HIDE_SILENT_1", ["F_HIDE"]),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
            "3": ("Etrafı Aramya başla.", "S16_CAFETERIA_CHESS_SETUP", []),
        },
    },

"S15_HIDE_SILENT_1": {
    "text": (
    "##Nefesini tutuyorsun||"
    "Nerdeyse hiç kıpırdmıyorsun||"
    "Hademe de kıpırdamıyor||"
    "Sanki zaten biliyor||"
    "Orada olduğunu||"
),"layout": "single",
    "images": [ "images/s15_hide_silent_1.png"],
    "choices": {
        "1": ("Sessiz kal / kıpırdama", "S15_HIDE_SILENT_2", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},

"S15_HIDE_SILENT_1_DUO": {
    "text": (
    "##Nefesini tutuyorsun||"
    "Nerdeyse hiç kıpırdmıyorsunuz||"
    "Hademe de kıpırdamıyor||"
    "Sanki zaten biliyor||"
    "Orada olduğunuzu||"
),"layout": "single",
    "images": [ "images/s15_hide_silent_1.png"],
    "choices": {
        "1": ("Sessiz kal / kıpırdama", "S15_HIDE_SILENT_2_DUO", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
    },
},

"S15_HIDE_SILENT_2": {
    "text": (
    "##Parmakların istemsiz titriyor ama durduruyorsun||"
    "Ayakkabı sesi bir adım sağa kayıyor... sonra geri geliyor||"
    "Olduğu yerde git gel yapıyor.[[BLINK]]□|||"

    "Olacakları biliyor gibi||"
),
"layout": "single",
    "images": [ "images/s15_hide_silent_2.png"],
    "choices": {
        "1": ("Sessiz kal / dayan", "S15_HIDE_FORCED", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},

"S15_HIDE_SILENT_2_DUO": {
    "text": (
    "##Parmakların istemsiz titriyor ama durduruyorsun||"
    "Ayakkabı sesi bir sağa gidyor bire sola ||"
    "Olduğu yerde git gel yapıyor.[[BLINK]]□|||"

    "Olacakları biliyor gibi||"
),
"layout": "single",
    "images": [ "images/s15_hide_silent_2.png"],
    "choices": {
        "1": ("Sessiz kal / dayan", "S15_HIDE_FORCED_DUO", []),
        "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
    },
},

"S15_HIDE_FORCED": {
    "text": (
    "##Bukadar sessizlik yeter||"
    "Bu artık saklanmak değil||"
    "Önünde kıpırdamadan bekliyor||"
    "Resmen seninle oynuyor.[[BLINK]]□|||"

    "Saklanarak buradan çıkamayacağını anlıyorsun.[[BLINK]]"
),
"layout": "single",
    "images": [ "images/s15_hide_forced.png"],
    "choices": {
        "1": ("Karşısına çık  ", "S16_HADEME_SENI_GORDU", ["F_NOISE"]),
        "2": ("Dikkati başka yöne çek  (sesle)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
    },
},

"S15_HIDE_FORCED_DUO": {
    "layout": "single",
    "images": [ "images/s15_hide_forced_duo.png"],
    "text": (
    "##Bukadar sessizlik yeter||"
    "Bu artık saklanmak değil||"
    "Önünüzde kıpırdamadan bekliyor||"
    "Resmen sizinle oynuyor.[[BLINK]]□|||"

    "Saklanarak buradan çıkamayacağını anlıyorsunuz.[[BLINK]]"
),
    "choices": {
        "1": ("Karşısına çık   ", "S16_HADEME_SENI_GORDU_DUO", ["F_NOISE"]),
        "2": ("dikkati başka yöne çek  (sesle)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
        "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
    },
},

"S15_HIDE_DISTRACT": {
    "text": (
    "⊕##Etrafta bulduğun metal bi şişeyi fırlatttın... küçük ama yeterli||"
    "##Hademe başını aniden çeviriyor||"
    "'Güzel... sonunda bir kaçmak için bi fırsat.[[BLINK]]□|||"

    "'Tam zamanı bi anda fırlıyosun||"
    "Ama hademe bunu farkediyo.[[BLINK]]'□|||"

    "Olabildiğinde hızlı kafeteryanın kapısından kaçmaya çalışıyosun||"
    "##Ama  bunu düşünüp kapıyı kitlemiş||"
    "Sen daha ne olduğnun bile anlamadan seni yakalıyo||"
    "[[BLACK1000]]"
), "inline_symbol_sfx": {
        "⊕": "sounds/throwing.mp3"
    },
    "images": [
        "images/s15_distract_duo_1_throw.png",
        "images/s15_distract_duo_2_locked_door.png",
        "images/s15_distract_duo_3_caught.png",
    ],

    "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
    "auto_next_after": True,
    "auto_next_delay_ms": 500,
},

"S15_HIDE_DISTRACT_DUO": {
    "text": (
    "⊕##Etrafta bulduğun metal bi şişeyi fırlatttın... küçük ama yeterli||"
    "##Hademe başını aniden çeviriyor||"
    "'Güzel... sonunda bir kaçmak için bi fırsat.[[BLINK]]□|||"

    "'1□ 2 □3 fırla||"
    "Ama hademe bunu farkediyiyo.[[BLINK]]'□|||"

    "Olabildiğinde hızlı kafeteryanın kapısından kaçmaya çalışıyosunuz||"
    "##Ama bunu düşünüp kapıyı kitlemiş||"
    "Daha ne olduğnun bile anlayamada sizi yakalıyo||"
    "[[BLACK1000]][[BLINK]]"
),"inline_symbol_sfx": {
        "⊕": "sounds/throwing.mp3"
    },
    "images": [
        "images/s15_distract_duo_1_throw.png",
        "images/s15_distract_duo_2_locked_door.png",
        "images/s15_distract_duo_3_caught.png",
    ],

    "auto_next": "S15_CAFETERIA_STORAGE_DUO",
    "auto_next_after": True,       # ✅ metin bittikten sonra
    "auto_next_delay_ms": 500,      # ✅ bitince 500ms bekle
},
"S15_CAFETERIA_STORAGE": {
    "layout": "single",
    "image": "images/s15_cafeteria_storage_duo.png",  # tek büyük görsel

    "text": (
    "##Depoya atılıyorsun||"
    "Orda kendini görüyorsun||"
    "⊕Kilit sesi… kapıyı üstüne kapatıyor.[[BLINK]]□|||"

    "Kendinle başbaşa konuşmaya başlıyorsun.[[BLINK]]□|||"

    "-O hademede sanada garip gelen bişey yokmu||"
    "Tanıdık bişey.[[BLINK]]□|||"

    "-Dur tahmin ediyim ?\"||"
    "Aynı zamanda 3 farklı zaman kopyası||"
    "Neden burdasın||"
    "Ve asıl soru  neden 3 farklı zaman birbiri içinde.[[BLINK]]□|||"

    "-O kadarını bilmiyorum ||"
    "Tek bildiğim seni burda tutmak istiyo .[[BLINK]]□|||"

    "Ve benim seni burda çıkarmam gerek .[[BLINK]]□|||"

    "-Ama bunu nasıl yapıcaz||"
),"inline_symbol_sfx": {
        "⊕": "sounds/door_closing.mp3"
    },
    "choices": {
        "1": ("Havalandırmayı kullan", "S15_RAY_VENT_ESCAPE_SOLO", []),
        "2": ("Hademeye seslen", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
        "3": ("Sessiz kal", "S15_STORAGE_LISTEN", []),
    },
},
"S15_CAFETERIA_STORAGE_DUO": {
    "layout": "single",
    "image": "images/s15_cafeteria_storage_duo.png",  # tek büyük görsel

    "text": (
    "##Depoya atılıyorsun. orda kendini görüyorsun||"
    "⊕Kilit sesi… kapıyı üstüne kapatıyor.[[BLINK]]□|||"

    "Kendinle başbaşa konuşmaya başlıyorsun.[[BLINK]]□|||"

    "-O hademede sanada garip gelen bişey yokmu||"
    "Tanıdık bişey.□.[[BLINK]]□|||"

    "-Ne gibi ???□||"
    "Konuşması□||"
    "Görünüşü□||"
    "Duruşu□.[[BLINK]]□|||"

    "7sinde 70 indede oyuz||"
    "-Yoksa||"
    "Ama nasıl olur||"
    "Aynı zamanda 3 farklı zaman kopyası.[[BLINK]]□|||"

    "Neden burdasın||"
    "Ve asıl soru||"
    "Neden 3 farklı zaman birbiri içinde.[[BLINK]]□|||"

    "-O kadarını bilmiyorum.□||"
    "Tek bildiğim seni burda tutmak istiyo.[[BLINK]]□|||"

    "Ve benim seni burda çıkarmam gerek.□||"
    "-Ama bunu nasıl yapıcaz||"
),"inline_symbol_sfx": {
        "⊕": "sounds/door_closing.mp3"
    },
    "choices": {
        "1": ("Havalandırmayı kullan", "S15_RAY_VENT_ESCAPE_SOLO", []),
        "2": ("Hademeye seslen", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
        "3": ("Sessiz kal", "S15_STORAGE_LISTEN", []),
    },
},


        "S15_CAFETERIA_STORAGE_LOCK": {
        "text": (
    "Deponun kapısına kulağının dayadın||"
    "İçerden bi ses geliyo.[[BLINK]]□|||"

    "Tanıdık bi ses||"
    "Anahtar kapının üzerinde.[[BLINK]]"
),
        "choices": {
            "1": ("Tek başına yangın çıkışına git", "END_SOLO_ESCAPE_A", []),
            "2": ("Kapıyı aç", "S15_CAFETERIA_STORAGE", []),
           
        },
    },
       
        
    "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR": {
        "text": (
    "##Tamam.Dinle||"
    "Onu yenemeyiz.|Ama onu ikna etmeye çalışabiliriz.[[BLINK]]□|||"

    "-Nasıl||"
    "-Bilmiyorum.[[BLINK]]□|||"

    "Önce bi ne olup bittiğini anlamamız gerek||"
    "Buyüzden  Onunla konuşmalıyız||"
    "Kapıyı tıklatıyorsun.[[BLINK]]□|||"

    "⊕Tak||"
    "Tak||"
    "Tak.[[BLINK]]□|||"

    "Hademe Kapıyı açıyor||"
    "-Ne istiyorsunuz||"
    "-Bizi neden burada tutuyorsun.[[BLINK]]□|||"

    "-Bazı şeyleri açıklamakla zaman kaybedemem||"
    "-Bizi sonsuza kadar burda tutamazsın||"
    "-Aslında yapabilirim||"
    "-Hayır yapamazsın aynı zamanda 3 farklı varyantın bulunmasının risklerini biliyosun||"
    "-Bana akıl verme dopru olanı yapıyorum.[[BLINK]]□|||"

    "-Çocuğun burdan gitmesi gerek||"
    "-Bunun olmucağını biliyosun||"
    "Neden olamıcağınıda.[[BLINK]]□|||"

    "Sen'burda neler oluyo:||"
    "-Anlat ona||"
    "-Tamam.[[BLINK]]□|||"

    "Ama bunun hoşuna gidiceğini sanmıyorum ||"
    "Şuan geçmiş ve gelecek senin burda kalmana bağlı ||"
    "Sen bir anomalisin zamanı bir arada tutuyorsun -Peki neden ben||"
    "-Çünkü hepsi benim hatam.[[BLINK]]□|||"

    "Ve sen bensin||"
    "Burdan çıkmıyorsun||"
    "Deyip kapıyı üzerine kapıyı kapatmak||"
    "İçin arkasını dönüyor ve çıkmaya hazırlanıyor||"
),  "inline_symbol_sfx": {
        "⊕": "sounds/knocking_door.mp3"
    },
        "choices": {
            "1": ("İtiraz et", "S18_ARGUE_WITH_JANITOR", []),
            "2": ("Hademeye saldır", "S18_ATTACK_JANITOR", []),
            "3": ("Orada kalmaya karar ver", "S18_DECIDE_STAY", []),
        },
    },

"S18_ARGUE_WITH_JANITOR": {
    "layout": "single_focus",
    "image": "images/end_locked_for_time.png",

    "text": (
        "-Hayır||"
        "Bu benim hatam değil||"
        "Hademe gözlerini kısıyor…||"
        "Hıh. Başka çaren yok.[[BLINK]]□|||"
        "Duvardaki saate bakıyorsun.||"
        "02:17||"
        "02:17||"
        "Ve hep 02:17.||"
        "Zamanda sıkışıp kaldın.||"
        "En azından yalnız değilsin.[[BLINK]]"
    ),

    "scene_music": "sounds/ending_ticking.mp3",
    "scene_music_volume": 0.20,

    "ending": True,
    "ending_id": "END_LOCKED_FOR_TIME",

    "ending_sequence_cfg": {
        "images": [
            "images/end_locked_for_time.png",
        ],
        "final_title": "ENDING  —  ZAMANA KİLİTLİ",
        "final_line": "Zaman hiç değişmez.",
        "fade_in_ms": 2000,
        "fade_out_ms": 2200,
        "final_hold_ms": 2000,
        "typewriter_speed": 55,
        "next_scene": "LOBBY",
    },
},
"S18_DECIDE_STAY": {
    "layout": "single_focus",
    "image": "images/end_locked_for_time.png",

    "text": (
        "Yapabileceğimiz bir şey yok||"
        "Onu durduramayız||"
        "Hademe gözlerini kısıyor…[[BLINK]]□|||"
        "Ben de öyle düşünmüştüm.||"
        "Duvardaki saate bakıyorsun.||"
        "02:17||"
        "02:17||"
        "Ve hep 02:17.||"
        "Zamanda sıkışıp kaldın.||"
        "En azından yalnız değilsin.[[BLINK]]"
    ),

    "scene_music": "sounds/ending_theme_locked.mp3",
    "scene_music_volume": 0.20,

    "ending": True,
    "ending_id": "END_LOCKED_FOR_TIME",

    "ending_sequence_cfg": {
        "images": [
            "images/end_locked_for_time.png",
        ],
        "final_title": "Zamanda mahsur",
        "final_line": "02:17 artık hiç bitmeyecek Asla .",
        "fade_in_ms": 2000,
        "fade_out_ms": 2000,
        "final_hold_ms": 2400,
        "typewriter_speed": 55,
        "next_scene": "LOBBY",
    },
},
"S18_ATTACK_JANITOR": {
    "text": (
        "Hayır.[[BLINK]]□|||"
        "Bu benim hatam değil||"
        "Böyle bitemez deyip saldırıyorsun…||"
        "##Seni geçen seferki gibi kolayca itiyor.[[BLINK]]□|||"
        "Ama bu sefer yalnız değilsin||"
        "Senin itildiğin esnada arkandan genç halin gelip||"
        "##Sağlam bir yumruk atıyor||"
        "Yalpalayıp yere düşüyor.[[BLINK]]□|||"
        "Bu ikiniz için de bir fırsat.||"
        "Hemen koridora koşuyorsunuz||"
        "Koridor boyunca ayak sesleriniz yankılanıyor||"
        "Yangın çıkışına doğru||"
        "Çıkışa vardığında cebinden anahtarı çıkarıp kilide takıyorsun||"
        "##Yangın çıkışının kapısı açıldığında bir zaman portalı çıkıyor.[[BLINK]]"
    ),

    "images": [
        "images/s18_attack_janitor_1_fall.png",
        "images/s18_attack_janitor_2_run.png",
        "images/image_copy.png",
    ],

    "choices": {
        "1": ("Genç halini tut ve portala atla", "END_ATTACK_PORTAL_JUMP", []),
        "2": ("Tek başına git", "END_ATTACK_SURRENDER", []),
        "3": ("Hademeyi ikna et", "END_ATTACK_DISARM_ATTEMPT", []),
    },
},
# 1) PORTALA SIÇRAMA (3 görsel) -> auto_next: WHITE_ROOM
"END_ATTACK_PORTAL_JUMP": {
    "text": (
    "##Genç halinin bileğini bakıyorsun.[[BLINK]]□|||"

    "ŞİMDİ!□KOOOŞ□||"
    "Bir an bile tereddüt etmiyor.[[BLINK]]□|||"

    "##İkiniz birden portala atlıyorsunuz||"
    "-HAYIR!!!||"
    "Bunun olmasına izin veremem||"
    "##Deyip arkanızdan atlıyor||"
),
    "images": [
        "images/end_duo_two_leave_1_dash_into_portal.png",
        "images/end_duo_two_leave_2_time_layers_flash.png",
        "images/end_attack_portal_jump_3_follow.png",
    ],
    "scene_music": "sounds/ending_theme6.mp3",
    "scene_music_volume": 0.20,

    "auto_next": "END_ATTACK_WHITE_ROOM",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
    "ending_id": "END_ATTACK_PORTAL_JUMP",
},


"END_ATTACK_WHITE_ROOM": {
    "text": (
    "##Burası da neresi.□||"
    "Ses yok.□Yankı yok||"
    "Sadece beyaz.[[BLINK]]□|||"

    "##İleride bi kapı var□||"
    "##Yaklaşıp kapıyı çalışıyolarsunuz□||"
    "⊕Tak□ tak□||"
    "Durun bisaniye□||"
    "Kapıya bakmalyım.[[BLINK]]"
), "inline_symbol_sfx": {
        "⊕": "sounds/knocking_door.mp3"
    },
        
    "images": [
        "images/end_attack_white_room_1_arrive.png",
        "images/end_attack_white_room_2_void.png",
        "images/end_attack_white_room_3_door_far.png",
    ],
    "auto_next": "END_ATTACK_NARRATOR_DOOR_SINGLE",
    "auto_next_after": True,
    "auto_next_delay_ms": 1000,
},
"END_ATTACK_NARRATOR_DOOR_SINGLE": {
    "layout": "single_focus",
    "image": "images/end_attack_narrator_room_single.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_ATTACK_NARRATOR_ENDING",

    "ending_sequence_cfg": {
        "images": [
            "images/end_attack_door_single.png",
            "images/end_attack_narrator_room_single.png",
        ],
        "holds_ms": [3000, 3000],

        "instant_switch": False,
        "direct_cut_between_images": True,

        "fade_in_ms": 1200,
        "fade_out_ms": 1000,
        "fade_steps": 32,
        "cover": True,

        "overlay_texts": [
            "Ah çocuklar...|||",
            "Siz mi geldiniz?|||"
        ],

        "overlay_type_ms": 55,
        "overlay_seg_pause_ms": 760,
        "overlay_page_pause_ms": 700,
        "overlay_box_pause_ms": 1200,

        "next_scene": "LOBBY",
    },

    "final_screen_line": "Bende sizi bekliyordum",
    "ending_title": "Matrix Sonu",

    "final_type_ms": 55,
    "final_hold_ms": 0,
    "final_fade_ms": 0,
    "title_pop_steps": 10,
},
# 1) END_ATTACK_SURRENDER -> 3 görsel -> auto_next: YATAK (tekli)
"END_ATTACK_SURRENDER": {
    "text": (
    "##Genç halin sana bakıyor||"
    "Git||"
    "##Ben onu oyalarım.[[BLINK]]□|||"

    "##Vakit yok. Çabuk.[[BLINK]]"
),
    "images": [
        "images/end_attack_surrender_1_look.png",
        "images/end_attack_surrender_2_push.png",
        "images/end_attack_surrender_3_turn.png",
    ],
    "auto_next": "END_WAKE_BED_2016_SINGLE",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
    "ending_id": "END_ATTACK_SURRENDER",
},

# 2) Yatakta uyanma (20:16) -> tek büyük görsel + TEK seçenek: "Koridora çık"
"END_WAKE_BED_2016_SINGLE": {
    "layout": "single",
    "image": "images/end_wake_2016_bed.png",
    "text": (
    "##Gözlerini açıyorsun.[[BLINK]]□|||"

    "Yatak. Oda .[[BLINK]]□|||"

    "Başını çeviriyorsun…[[BLINK]]□|||"

    "##Saat: 02:16.[[BLINK]]"
),
    "choices": {
        "1": ("Koridora çık", "END_WAKE_CORRIDOR_3", []),
    },
},

# 3) (İKİNCİ SAHNE: Koridora çık) -> 3 görsel
"END_WAKE_CORRIDOR_3": {
    "text": (
    "Bişeyler çok yanlış gitmiş .[[BLINK]]"
),
    "images": [
        "images/end_wake_corridor_2.png",
    ],
    "ending_id": "END_WAKE_CORRIDOR_3",
},

    "END_ATTACK_DISARM_ATTEMPT": {
        "text": (
    "Bunu sen başlattın sen bitirmek zorundasın ||"
    "Zamanın nasıl işlediğini biliyosun||"
    "Yaptıklarının bedelini ödemeden gerek.[[BLINK]]□|||"

    "Demedinmi sanıyosun||"
    "Sadece işleri dahada karşmalıklaştırıyor||"
    "Tek bi farkla.[[BLINK]]□|||"

    "Artık ne yapmam gerektiğini biliyosun:||"
    "Birbirinize bakıyorsunuz ve anlıyor…||"
    "Kafasıyla onaylıyor…||"
    "Yavaş yavaş portaldan geçerken||"
    "Son bi kez kafasını çevirip bakıyor …||"
    "Yaptıklarının sonuçlarının farkında'.[[BLINK]]□|||"

    "Ama elinden gelen tek şey (devam etmek.[[BLINK]])"
),
        "ending_id": "END_ATTACK_DISARM_ATTEMPT",
            "images": [
        "images/end_attack_disarm_1_look.png",
        "images/end_attack_disarm_2_silence.png",
        "images/end_attack_disarm_3_nod.png",
    ],
    },

"S15_RAY_VENT_ESCAPE_SOLO": {
    "images": [
        "images/s15_vent_escape_left.png",
        "images/s15_vent_escape_mid.png",
        "images/s15_vent_escape_right.png",
    ],
    "text": (
    "Gözlerin karanlığa alışırken□||"
    "Arkandaki metal ızgarayı fark ediyorsun.□||"
    "##Sürünerek içeri giriyorsun.□||"
    "##Omuzların zar zor sığıyor.[[BLINK]]□|||"

    "Karanlık bir tünel||"
    "Her hareketinde metal inliyor.□||"
    "Bir yerde tünel ikiye ayrılıyor gibi.□||"
    "##Önünde koridora açılan bir ızgara var...[[BLINK]]□|||"
),
    "auto_next": "S15_VENT_DROP_AUTO",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},

"S15_VENT_DROP_AUTO": {
    "layout": "single",
    "image": "images/s15_vent_drop.png",
    "text": (
    "Kapağı itiyorsun.□||"
    "##Kendini aşağı doğru bırakıyorsun.□||"
    "Ayakların yere değiyor.[[BLINK]]□|||"

    "Bir an dengen kayıyor.□||"
    "Sonrası sessizlik.□||"
    "Kafeterya koridoru.[[BLINK]]□|||"
),
    "auto_next": "END_SOLO_ESCAPE_A_2",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},



    "S16_CHESS_PUZZLE_SCREEN": {
        "layout": "single_focus",
        "images": [ "images/s16_chess_puzzle_screen.png"],
        "text": (
    "##Tahtaya bakıyorsun||"
    "Taşlar sana bir şey ima ediyor.[[BLINK]]□|||"

    "Oyun sonu çok yakın gibi||"
    "Taşların koordinatları sana bir şeyler anlatıyor||"
    "Şifre bu olabilir mi?||"
    "Ama hangi taş ve hangi koordinat?[[BLINK]]□|||"

    "Biraz düşündükten sonra fark ediyorsun:||"
    "BULDUM! Tek hamlede mat var.[[BLINK]]□|||"

    "ŞİFRE BU OLMALI.[[BLINK]]"
),
        "choices": {
            "1": ("Kale h7'ye oynar","S16_CHESS_TRY_A", []),
            "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
            "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
        },
    },

    "S16_CHESS_TRY_A": {
        "layout": "single_focus",
        "images": ["images/s16_chess_try_a.png"],
        "text": (
    "##Kale h7 gibi ama emin değilim||"
    "Ozaman şifre h7 olabilirmi||"
    "Denemekten zarar gelmez herhalde:||"
),
        "choices": {
            "1": ("Şifreyi deneyelim bakalım", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_CHESS_TRY_B": {
        "layout": "single_focus",
        "images": [ "images/s16_chess_try_b.png"],
        "text": (
    "##Atı g6'ya oynuyorsun||"
    "Ozaman şifre g6 olabilirmi||"
    "Denemekten zarar gelmez herhalde:||"
),
        "choices": {
            "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_CHESS_TRY_C": {
        "layout": "single_focus",
        "images": [ "images/s16_chess_try_c.png"],
        "text": (
    "##Atı f7'ya oynuyorsun||"
    "Ozaman şifre f7 olabilirmi||"
    "Denemekten zarar gelmez herhalde||"
),
        "choices": {
            "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_UNLOCK_SEQUENCE": {
        "layout": "single_focus",
        "images": [ "images/s16_1_counter_back_copy.png"],
        "text": (
    "##Tezgâhın altına eğiliyorsun||"
    "Şifreli olan kilidi şifreni girmeye hazırlanıyorsun||"
),

        "choices": {
            "1": ("h7 ", "S16_kilit_açılmıyor_a", []),
            "2": ("g6", "S16_şifre_doğru", []),
            "3": ("f7", "S16_kilit_açılmıyor_c", []),
        },
    },

    "S16_kilit_açılmıyor_a": {
        "text": (
    "##Yanlış hesaplamış olmalıyım||"
    "Bidaha denemeliyim||"
    
),"images": [ "images/s16_kilit_acilmiyor_a.png"],
"layout": "single_focus",
        "choices": {
            "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_Again", []),
            "2": ("Yangın söndürücüyü al", "S16_şifre_doğru", []),
            "3": ("SAKLAN !!!", []),
        },
    },
        "S16_kilit_açılmıyor_c": {
        "text": (
    "##Yanlış hesaplamış olmalıyım||"
    "Bidaha denemeliyim||"
),"images": [ "images/s16_kilit_acilmiyor_c.png"],
 "layout": "single_focus",
        "choices": {
            "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_Again", []),
            "2": ("Yangın söndürücüyü al", "S16_şifre_doğru", []),
            "3": ("SAKLAN !!!", []),
        },
    },
    "S16_CHESS_PUZZLE_SCREEN_Again": {
        "layout": "single_focus",
        "images": [ "images/s16_chess_puzzle_screen.png"],

        "text": (
    "##Tekrar tahtaya bakıyorsun||"
    "Bu sefer doğru hamleyi yapman gerek.[[BLINK]]"
),
        "choices": {
            "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A", []),
            "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
            "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
        },
    },

    "S16_şifre_doğru": {
        "text": (
    "##Biliyordum||"
    "Kilit açıldı||"
    "İçinde bir anahtar var||"
    
),"images": [ "images/s16_sifre_dogru.png"],
    "layout": "single_focus",
        "choices": {
            "2": ("Anahtarı al", "S16_KEY_TAKEN_SOLO", ["I_KEY"]),
        },
    },
    "S16_şifre_doğru_DUO": {
        "text": (
    "##Biliyordum||"
    "Kilit açıldı||"
    "İçinde bir anahtar var||"
),"images": [ "images/s16_sifre_dogru_duo.png"],
"layout": "single_focus",

        "choices": {
            "2": ("Anahtarı al", "S16_KEY_TAKEN_DUO", ["I_KEY"]),
        },
    },
"S16_KEY_TAKEN_DUO": {
    "layout": "single",
    "text": (
    "##Anahtarı aldın||"
    "Ne açtığını bilmiyorsun||"
    "Gelecekteki halin yanına geliyor||"
    "Yangın çıkışı.[[BLINK]]□|||"

    "Yan taraftaki kapıdan bir ses geliyor||"
    "Hafif bir tıkırtı||"
    "Sanki kapının arkasında biri var||"
    "Kafeterya koridoru ise bomboş||"
    "Işıklar titriyor.[[BLINK]]□|||"
),
    "image": "images/s16_key_taken_duo.png",
    "choices": {
        "1": ("Yangın çıkışına gidin", "S17_DUO_ESCAPE_RUN", []),
        "2": ("Ses gelen kapıya yaklaşın ", "S16_DUO_CHECK_SOUND", []),

    },
},
    "S16_KEY_TAKEN_SOLO": {
        "text": (
    "##Anahtarı aldın||"
    "Ne açtığını bilmiyorsun||"
    "Tam cebine koyacakken…[[BLINK]]□|||"

    "Yan taraftaki kapıdan bir ses geliyor||"
    "Hafif bir tıkırtı||"
    "Sanki biri kapının arkasında biri var.[[BLINK]]□|||"

    "Kafeterya koridoru ise bomboş||"
    "Işıklar titriyor.[[BLINK]]"
),"images": [ "images/s16_key_taken_solo.png"],
"layout": "single_focus",

        "choices": {
            "1": ("Yangın çıkışına doğru git", "END_SOLO_ESCAPE_A", []),
            "2": ("Ses gelen kapıya doğru yaklaş", "S16_RAY_TO_S15_CAPTURE", []),
        },
    },

"S16_RAY_TO_S15_CAPTURE": {
    "text": (
    "##Kapıya yaklaşıyorsun||"
    "Ses çok yakın..||"
    "Elin, istemsizce anahtarı sıkıyor||"
    "Metal avucunda sıkıca duruyor.[[BLINK]]□|||"

    "Kulağını kapıya yaklaştırıyorsun||"
    "İçeriyi duymak için||"
    "Ve tam o an...[[BLINK]]□|||"

    "Arkandan bir gölge düşüyor||"
    "Ne olduğunu anlamadan bileğin kavranıyor.[[BLINK]]□|||"

    "Hademe||"
    "Tek kelime etmeden seni tutuyor.[[BLINK]]□|||"

    "⊕Kapıyı açıp||"
    "Seni içeri itiyor..||"
    "✦Kapıyı üstüne kapatıyor||"
    "Kilit sesi.[[BLINK]]□|||"
),
   "inline_symbol_sfx": {
        "⊕": "sounds/door_opening.mp3",
        "✦": "sounds/door_closing.mp3"
        
    },

    "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},
"END_SOLO_ESCAPE_A": {
    "layout": "single_focus",
    "image": "images/scene_corridor.png",
    "flicker": {"index": 2, "slot": "C", "intensity": "strong"},

    "text": (
    "##Kafeteryadan fırlıyorsun||"
    "Koridorun ucunda, paslı bir tabela||"
    "YANGIN ÇIKIŞI.[[BLINK]]□|||"

    "Kapının etrafındaki ışık diğerlerinden farklı...□||"
    "Garip bi his veriyo.[[BLINK]]□|||"
),

    "auto_next": "END_SOLO_ESCAPE_B",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},
"END_SOLO_ESCAPE_A_2": {
    "layout": "single_focus",
    "image": "images/scene_corridor.png",
    "flicker": {"index": 2, "slot": "C", "intensity": "strong"},

    "text": (
    "##Havalandırmadan iniyorsun||"
    "Koridorun ucunda, paslı bir tabela||"
    "YANGIN ÇIKIŞI.[[BLINK]]□|||"

    "Kapının etrafındaki ışık diğerlerinden farklı...□||"
    "Garip bi his veriyo.[[BLINK]]□|||"
),

    "auto_next": "END_SOLO_ESCAPE_B",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},
"END_SOLO_ESCAPE_B": {
    "layout": "single_focus",
    "image": "images/scene_cafeteria_janitor.png",
     "flicker": {"index": 2, "slot": "C", "intensity": "strong"}
,

    "text": (
    "Arkana bakıyorsun□||"
    "Hademe orada.[[BLINK]]□|||"

    "Yaşlı… □omuzları çökmüş… □ama gözleri keskin||"
    "Koşamıyor.□||"
    "Ama seni durdurmaya çalışıyor.[[BLINK]]□|||"
),

    "auto_next": "END_SOLO_ESCAPE_C",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},


# 3) FIRE EXIT
"END_SOLO_ESCAPE_C": {
    "layout": "single_focus",
    "image": "images/scene_fire_exit_door.png",
    "text": (
    "Kapıya doğru hızlanıyorsun.□||"
    "Elin kolun titreyerek anahtarı çıkarıyorsun.□.[[BLINK]]□|||"

    "Kilit…□||"
    "✦Tık.[[BLINK]]□|||"

    "Kapıyı açıyorsun □||"
    "Bu bir kapı değil.[[BLINK]]□|||"
),"inline_symbol_sfx": {
    "✦": {"path": "sounds/door_lock.mp3", "volume":1}
},

    # ✅ otomatik sonraki sahne (metin bitince)
    "auto_next": "END_SOLO_ESCAPE_D",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},


"END_SOLO_ESCAPE_D": {
    "layout": "single_focus",

    # ✅ fallback görsel: gerçekten var olan bir PNG olmalı
    # sende bg.png var görünüyor, istersen onu koy:
    "image": "images/image_copy.png",

    # ✅ MP4 oynat
    "video": {
        "path": "images/portal_anim/portal.mp4",
        "fps": 24,
        "loop": True
    },

    "text": (
    "##Kapının içinde… □dönüp duran bir boşluk var||"
    "Işık değil□— sanki zamanın kendisi kıvrılıyor||"
    "Bir ZAMAN PORTALI.[[BLINK]]□|||"

    "Hademe arkanıdan bağırıyor □||"
    "Dur!□||"
    "Her şeyi mahvedeceksin![[BLINK]]□|||"

    "Sesi çatlıyor.□||"
    "Portaldan bi adım uzaktasın||"
),
    "choices": {
        "1": ("Hademeye neler olup bittiğini sor", "END_SOLO_ESCAPE_ASK", []),
        "2": ("Kapıdan geç", "END_SOLO_ESCAPE_PORTAL_VIDEO", []),
    },
},
"END_SOLO_ESCAPE_PORTAL_VIDEO": {
    "layout": "single_focus", 
    "image": "images/portal_copy.png",

     # ✅ şart
    "video": {"path": "images/videos/portal_end.mp4", "fps": 24, "loop": True},

    "scene_music": "sounds/ending_portal_loop.mp3",
    "scene_music_volume": 0.25,

    "text": (
    "Portal önünde dalgalanırken□||"
    "Senin aklında tek birşey var□||"
    "Bir an önce burdan kurtulmak□||"
),

    "auto_next": "END_SOLO_ESCAPE_PORTAL",
    "auto_next_after": True,
    "auto_delay_ms": 1000,
    "auto_next_delay_ms": 0,
},
"END_SOLO_ESCAPE_PORTAL": {
    "layout": "triptych",
    "images": [
        "images/end_portal_after_1.png",
        "images/end_portal_after_2.png",
        "images/end_portal_after_3.png",
    ],

    # burada scene_music YOK -> önceki müzik devam eder

    "text": (
    "##Portala bakıyorsun□||"
    "Gözlerin keskin□||"
    "##Portalda gelen uçsuz bucaksız□||"
    "Zamanın akışında kaybolurken.[[BLINK]]□|||"

    "Derin bi nefes çekip□||"
    "##Kendini akıp giden portalın içine bırakıyorsun||"
),



    "auto_next": "END_SOLO_ESCAPE_PORTAL_ENDING",
    "auto_next_after": True,
    "auto_delay_ms": 1000,
    "auto_next_delay_ms": 0,
},

"END_SOLO_ESCAPE_PORTAL_ENDING": {
    "layout": "triptych",

    "images": [
        "images/end_ending_1.png",
        "images/end_ending_2.png",
        "images/end_ending_3.png",
    ],

    "text": (
    "##Gözlerini açıyorsun.□||"
    "Yatak||"
    "Tavan||"
    "##Aynı oda.[[BLINK]]□|||"

    "Her şey… aynı.□||"
    "Bunun her şeyi yok etmesi gerekmiyor muydu.□||"
    "Doğrulup saate bakıyorsun.□||"
    "##Saat: 02:18.[[BLINK]]□|||"

    "Ama ne oldu, her şey yoluna mı girdi?||"
    "Tam o sırada bir ses duyuyorsun…[[BLINK]]□|||"
),

    "auto_next": "END_SOLO_ESCAPE_PORTAL_ENDING_FINAL",
    "auto_next_after": True,
    "auto_next_delay_ms":500,
},
"END_SOLO_ESCAPE_PORTAL_ENDING_FINAL": {
    "layout": "single_focus",
    "image": "images/end_ending_final.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_SOLO_ESCAPE_PORTAL2",

    "ending_sequence_cfg": {
        "images": [
            "images/intro_building1.png",
        ],
        "holds_ms": [1500],

        "instant_switch": False,
        "fade_in_ms": 600,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,

        "next_scene": "LOBBY",
    },

    "final_screen_line": "Herşey yeni başlıyor",
    "ending_title": "Basit Son",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,
},

"END_SOLO_ESCAPE_ASK": {
    "layout": "single",
    "image": "images/end_solo_escape_ask.png",

  "text": (
    "Yutkunuyorsun||"
    "Bunu neden yapıyorsun?||"
    "Bu kapı ne?||"
    "Neden bu zamanda sıkışıp kaldım?[[BLINK]]□|||"

    "Hademe birkaç adım daha atıyor||"
    "Nefes nefese… ama gözlerini senden ayırmıyor||"
    "Ben…||"
    "Cümle boğazında takılıyor||"
    "Ben, bunların hepsini ben başlattım.[[BLINK]]□|||"

    "Nasıl yani diye soruyorsun||"
    "Hiç geçmişe gidip bir şeyleri yeniden yazmak istedin mi?||"
    "Her şeyi düzeltmek…||"
    "Ben istedim.[[BLINK]]□|||"

    "Karımı ve kızımı kaybettikten sonra||"
    "Benim hatamdı.Onları korumalıydım||"
    "Ama yapamadım||"
    "Her şeyimi kaybetmiştim.[[BLINK]]□|||"

    "Ama bir gün ikinci bir şans yaratmanın mümkün olduğunu öğrendim||"
    "Karımı ve kızımı kurtarabilirdim||"
    "Öyle de yaptım||"
    "Zaman portalını o kaza gününe ayarladım||"
    "Nihayet o kazayı hiç yaşanmamış kılabilecektim.[[BLINK]]□|||"

    "Öyle de yaptım.[[BLINK]]□|||"

    "Bir süre mutluydum||"
    "Hayatım tekrar karımla ve kızımla mutlu olduğum günlere geri dönmüştü.[[BLINK]]□|||"

    "Sonra ne oldu?||"
    "Zamanla ilgili bilmen gereken şey şu||"
    "Ne kadar kurcalarsan o kadar kontrolden çıkar.[[BLINK]]□|||"

    "Bir süre sonra yaptığım değişikliğin bedelini ödedim||"
    "Kendi zamanım içine çöktü||"
    "Tamamen karanlık ve boş bir zaman…||"
    "Milyarlarca hayat… o zamanda yaşayan insanlar…||"
    "Kiminin geleceği, kiminin geçmişi…||"
    "Hepsi yok oldu. Zamanın içinde bir yarık açıldı.[[BLINK]]□|||"

    "Yaptığım hatayı fark ettiğimde her şey çok geçti||"
    "Ama yaptığım şeyi düzeltebilirdim.[[BLINK]]□|||"

    "30 yıl öncesine gittim||"
    "Genç halime bunu anlattım ve durması gerektiğini söyledim||"
    "Ama bunu anlayamayacak kadar kibirli ve toydu||"
    "Ben de ona engel olamayacak kadar yaşlıydım.[[BLINK]]□|||"

    "O yüzden daha da geçmişe gitmeye karar verdim||"
    "Yılanın başını küçükken ezmeye||"
    "Ama tam oradan ayrılırken genç halim beni takip etti||"
    "Ve bu zamanda sıkıştık… hepimiz.[[BLINK]]□|||"

    "Ve seni buradan kurtarıp yaptığım şeye engel olmaya çalışıyordu||"
    "O yüzden onu durdurdum.[[BLINK]]□|||"

    "Şimdi de seni durduracaM||"
    "Zamanı korumak zorundayım.[[BLINK]]"
),
        "choices": {
            "1": ("Kal ve zamanı koru", "END_SOLO_STAY_PROTECT_TIME_A", []),
            "2": ("Ayrıl ve özgür ol", "END_SOLO_ESCAPE_PORTAL_VIDEO2", []),
        },
    },

"END_SOLO_STAY_PROTECT_TIME_A": {
    "layout": "single_focus",  # ✅ tam ekran
    "image": "images/end_solo_stay_a_hand_reach.png",
    "text": (
    "##Hademe elini uzatıyor||"
    "Portal arkanda dönmeye devam ediyor.[[BLINK]]□|||"

    "Kapıyı kapatıyorsun||"
    "Ve kilitliyorsun.[[BLINK]]"
),

    # ✅ MÜZİK (bu ending akışının başında başlar)
    "scene_music": "sounds/ending_theme2.mp3",
    "scene_music_volume": 0.20,

    
    "auto_next": "END_SOLO_STAY_PROTECT_TIME_B",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},

"END_SOLO_STAY_PROTECT_TIME_B": {
    "layout": "single_focus",  # ✅ tam ekran
    "image": "images/scene_fire_exit_door.png",  # ✅ ortadaki görseli fullscreen göster
    "text": (
    "##İnsanlık için bunu yapmalıyım||"
    "Başka bir yol yok.[[BLINK]]"
),
    "images": [ "images/scene_fire_exit_door.png"],
      "layout": "single_focus",  # ✅ aynen duruyor

    "auto_next": "END_SOLO_STAY_PROTECT_TIME_ENDING",
    "auto_next_after": True,
    "auto_next_delay_ms": 200,
},

"END_SOLO_STAY_PROTECT_TIME_ENDING": {
    "layout": "single_focus",  # ✅ tam ekran
    "image": "images/end_solo_stay_year_4.png",  # fallback
    "text": "##",

    "ending": True,
    "ending_id": "END_SOLO_STAY_PROTECT_TIME",

    "ending_sequence_cfg": {
        "images": [
            "images/end_solo_stay_year_1.png",
            "images/end_solo_stay_year_2.png",
            "images/end_solo_stay_year_3.png",
            "images/end_solo_stay_year_4.png",
        ],
        "holds_ms": [3000, 3000, 3000, 3000],

        "instant_switch": False,
        "fade_in_ms": 3500,
        "fade_out_ms": 2000,
        "fade_steps": 128,

        "cover": True,        # ✅ zaten tam ekran
        "next_scene": "LOBBY",
    },

    "final_screen_line": "Zaman artık güvende.",
    "ending_title": "Fedakârlık Sonu",
    "final_type_ms": 55,
    "title_pop_steps": 10,
},
"END_SOLO_ESCAPE_PORTAL_VIDEO2": {
    "layout": "single_focus", 
    "image": "images/portal_copy.png",

     # ✅ şart
    "video": {"path": "images/videos/portal_end.mp4", "fps": 24, "loop": True},

    "scene_music": "sounds/ending_portal_loop.mp3",
    "scene_music_volume": 0.25,

    "text": (
    "Portal önünde dalgalanırken □||"
    "Senin aklında tek birşey var□||"
    "Bir an önce burdan kurtulmak□||"
),

    "auto_next": "END_SOLO_ESCAPE_PORTAL2",
    "auto_next_after": True,
    "auto_delay_ms": 1000,
    "auto_next_delay_ms": 0,
},


"END_SOLO_ESCAPE_PORTAL2": {
    "layout": "triptych",
    "images": [
        "images/end_portal_after_1.png",
        "images/end_portal_after_2.png",
        "images/end_portal_after_3.png",
    ],

    # burada scene_music YOK -> önceki müzik devam eder

    "text": (
    "##Portala bakıyorsun□||"
    "Gözlerin keskin□||"
    "##Portalda gelen uçsuz bucaksız||"
    "Zamanın akışında kaybolurken.[[BLINK]]□|||"

    "Derin bi nefes çekip□||"
    "##Kendini akıp giden portalın içine bırakıyorsun||"
),

    # ✅ buradan ENDING sahnesine otomatik geçiş
    "auto_next": "END_SOLO_ESCAPE_PORTAL_ENDING2",
    "auto_next_after": True,
    "auto_delay_ms": 1000,
    "auto_next_delay_ms": 0,
},

"END_SOLO_ESCAPE_PORTAL_ENDING2": {
    "layout": "triptych",

    "images": [
        "images/end_ending_1.png",
        "images/end_ending_2.png",
        "images/end_ending_3.png",
    ],

    "text": (
    "##Gözlerini açıyorsun.□||"
    "Yatak.□||"
    "Tavan||"
    "##Odanın kokusu.□.[[BLINK]]□|||"

    "Her şey… aynı.□||"
    "Bunun her şeyi yok etmesi gerekmiyor muydu.□||"
    "Doğrulup saate bakıyorsun.□||"
    "##Saat: 02:18.[[BLINK]]□|||"

    "Ama ne oldu,□ her şey yoluna mı girdi?□||"
    "Tam o sırada dışardan bir ses duyuyorsun…[[BLINK]]□|||"
),

    "auto_next": "END_SOLO_ESCAPE_PORTAL_ENDING2_FINAL",
    "auto_next_after": True,
    "auto_next_delay_ms": 1000,
},
"END_SOLO_ESCAPE_PORTAL_ENDING2_FINAL": {
    "layout": "single_focus",
    "image": "images/end_ending_final.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_SOLO_ESCAPE_PORTAL2",

    "ending_sequence_cfg": {
        "images": [
            "images/end_ending_final.png",
        ],
        "holds_ms": [1000],

        "instant_switch": False,
        "fade_in_ms": 600,
        "fade_out_ms": 600,
        "fade_steps": 64,
        "cover": True,

        "next_scene": "LOBBY",
    },

    "final_screen_line": "Zaman sıfırlandı.",
    "ending_title": "Normal Son",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,
},




"S09_LOOP_ROOM": {
    "text": (
    "##Yatağındasın||"
    "Aynı oda||"
    "Yine 02:17||"
    "Ama bu sefer fark ediyorsun||"
    "Neden zaman ilerlemiyo||"
),
"layout": "single_focus",
"images": [
    
        "images/s09_loop_room.png",
        
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla dışarı çıkı", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S09_LOOP_ROOM_after_cleaner_men": {
    "text": (
    "##Bir anda yüzüne doğru bir yumruk çıkardın||"
    "⊕[[BLACK2000.[[BLINK]]]]"
),    "inline_symbol_sfx": {
        "⊕": "sounds/punch.mp3"
    },
    "layout": "single_focus",
    "images": [
    
        "images/s09_after_cleaner_men.png",
    
    ],
    "auto_next": "S09_LOOP_ROOM_after_cleaner_men_MAIN",
    "auto_next_after": True,
    "auto_next_delay_ms": 0,
},
"S09_LOOP_ROOM_after_cleaner_men_MAIN": {
    "text": (
    "Seni odana geri postaladı||"
    "Bi hademe neden dövüşmeyi bilirki amk.[[BLINK]]"
),
"layout": "single_focus",
    "images": [
      # ('dövüş sahneleri')
        "images/s09_loop_room.png",
    
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk ve tekrar koridora çık", "S04_CORRIDOR_after_fight", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S04_CORRIDOR_after_fight": {
        "text": (
    "##Tekrar koridordasın||"
    "Ama busefer boş||"
    "Onu bulduğum yerde fena benzeticem||"
),
"layout": "single_focus",
        "images": [ "images/s04_corridor_empty.png"],
        "choices": {
            "1": ("Yangın merdivenine git", "S15_FIRE_EXIT", []),
            "2": ("Yemekhaneye yönel", "S16_CAFETERIA_FROM_FIGHT", []),
            "3": ("Odana geri dön", "S09_LOOP_ROOM_4", []),
        },
    },
"S09_LOOP_ROOM_1": {
    "text": (
    "##Yatağındasın||"
    "Aynı oda||"
    "Saat 02:17|||"
    "Dakikalar geçmiyor"
    "Telefonun ekranı bile aynı ||"
    "Sanki zaman durmuş gibi||"
),
"layout": "single_focus",
    "images": [ "images/s09_loop_room.png"],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},

"S09_LOOP_ROOM_2": {
    "text": (
    "##Yatağındasın||"
    "Aynı oda||"
    "Saat 02:17||"
    "Nefes alıp veriyorsun||"
    "Sıkıntıdan tavanı izliyorsun.[[BLINK]]"
),
"layout": "single_focus",
    "images": [ "images/s09_loop_room.png"],
    "choices": {
        "1": ("Zorla hatırlamaya çalış", "S10_MEMORY_GLITCH", []),
        "2": ("Ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Hiç hareket etme", "END_E02", []),
    },
},

"S09_LOOP_ROOM_3": {
    "text": (
    "##Yatağındasın||"
    "Aynı oda||"
    "Saat 02:17||"
    "Duvarlar hep bukadar dikkat çekimiydi||"
    "Ne diyorum ben||"
),
"layout": "single_focus",
    "images": [ "images/s09_loop_room.png"],
    "choices": {
        "1": ("Hatırayı zorla", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Gözlerini kapat", "END_E03", []),
    },
},

"S09_LOOP_ROOM_4": {
    "text": (
    "##Yatağındasın||"
    "Aynı oda||"
    "Saat 02:17||"
    "Oda bu sefer sessiz değil||"
),
"layout": "single_focus",
    "images": [ "images/s09_loop_room.png"],
    "choices": {
        "1": ("Artık kaçma", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E04", []),
    },
},


    "S10_MEMORY_GLITCH": {
        "text": (
    "##Başın dönüyor||"
    "Bir an her şey üst üste biniyor||"
    "##Koridor||"
    "Sesler||"
    "##Bir tartışma.[[BLINK]]"
),
"images": [
    "images/s10_glitch.png",     # SOL (blur loop bu olacak)
    "images/s10_center.png",     # ORTA (sabit)
    "images/s10_right.png",      # SAĞ (sabit)
],
        "choices": {
            "1": ("Kendini hatırlamaya zorla", "S14_PRE_CONFRONT", []),
            "2": ("Kendini durdur", "S09_LOOP_ROOM", []),
            "3": ("Sesin peşinden git", "S04_CORRIDOR", []),
        },
    },

"S11_CAMERA_ROOM": {
    "layout": "single_focus",
    "image": "images/s11_camera_room.png",
    "text": 
        "⊕##Kamera odasındasın.||"
        "Ekranlar açık.||"
        "Koridorda biri var.",
            "inline_symbol_sfx": {
        "⊕": "sounds/buzzing.mp3"
    },
        
        "choices": {
            "1": ("Kayıtları izle", "S11.1_CAMERA_REALIZATION", []),
            "2": ("Tüm Ekranları kapat", "END_E03", []),
            "3": ("Odadan çık", "S04_CORRIDOR_After_camera", []),
        },
    },
"S11.1_CAMERA_REALIZATION": {
    "layout": "single_focus",
    "image": "images/s11_camera_you.png",
    "text": (
    "⊕##Görüntüdeki kişi başını çeviriyor||"
    "Gözüküyor ama net değil.[[BLINK]]"
),
            "inline_symbol_sfx": {
        "⊕": "sounds/buzzing.mp3"
    },
        
    "choices": {
        "1": ("Zoom at", "S11.2_CAMERA_ZOOM", []),
        "2": ("Kamerayı kapat", "END_E03", []),
        "3": ("Geri çekil", "S04_CORRIDOR_After_camera", []),
    },
},

"S11.2_CAMERA_ZOOM": {
  "layout": "single_focus",
  "image": "images/s11_camera_you_close.png",
  "text": (
    "⊕##Yakınlaştırıyorsun||"
    "Pikseller büyüyor, görüntü daha da bozuluyor||"
    "Ama bir anlığına…||"
    "Yüz hatları tanıdık geliyor.[[BLINK]]□|||"

    "Çok tanıdık||"
    "Sanki aynaya bakmak gibi… ama değil.[[BLINK]]"
),            "inline_symbol_sfx": {
        "⊕": "sounds/buzzing.mp3"
    },
        
  "choices": {
    "1": ("Artık burada işin kalmadı, odadan çık", "S04_CORRIDOR_After_camera", []),
    "2": ("Bir kez daha zoom", "S11.3_CAMERA_AUTO_SHUTDOWN", [])
  },
}
,
"S11.3_CAMERA_AUTO_SHUTDOWN": {
    "layout": "triptych",
    "text": (
    "##Bir kez daha yakınlaştırmaya çalışıyorsun||"
    "Daha net görebilmek için||"
    "##Bir anda monitörler tek tek sönmeye başlar||"
    "##Cidden mi?[[BLINK]]□|||"

    "Bunun sırası mıydı…||"
    "Karanlıkta kalmak iyi bir fikir değil||"
    "Bir an önce buradan çıkmalıyım.[[BLINK]]"
),
    "images": [
        "images/s11_camera_room_left.png",      # 🟥 SOL: kamera odası / monitörler açık
        "images/s11_camera_shutdown.png",       # 🟥 ORTA: kapanan monitör (ana vurgu)
        "images/s11_dark_room_right.png",       # 🟥 SAĞ: karanlık oda / boşluk
    ],
    "choices": {
        "1": ("Çık", "S04_CORRIDOR_After_camera", []),
        "2": ("Kameraları tekrar açmaya çalış", "END_E03", []),
    },
},


"S12_CAMERA_HINT": {
  "layout": "single_focus",
  "image": "images/s12_camera_hint.png",
  "text": (
    "##Biri olup olmadığını kontrol ediyorsun||"
    "Yok gibi||"
    "Sanırsam||"
),
  "choices": {
    "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
    "2": ("Geri çekil", "S04_CORRIDOR_After_camera", []),
    "3": ("Bunu aklında tut", "S10_MEMORY_GLITCH", [])
  }
}
,

    # -------- PART 3 (TR) --------

 "S13_JANITOR_DIALOGUE": {
    "text": (
    "##Temizlikçi arabaya yaslanıp seni süzüyor||"
    "Yine mi sen? diyor||"
    "Geçen sefer de aynı saatti. 02:17||"
    "Yüzünde tatminsiz bir ifadeyle||"
    "Biraz da yorgun gibi||"
),
"layout": "single_focus",
    "images": [

        "images/s13_janitor_dialogue.png",

    ],
    "choices": {
        "1": ("Geçen sefer ne demek?", "S16_JANITOR_INFO", []),
        "2": ("Aniden kafeteryaya koş ", "S8.6_go_to_caffeteria", []),
        "3": ("Yalan söylediğini ima et", "S8.4_ANSWER_HİM2", []),
    },
},

    "S8.4_ANSWER_HİM2": {
        "text": (
    "##YALAN SÖYLÜYORSUN||"
    "Sana güvenmiyorum.[[BLINK]]□|||"

    "Bunu pek hoş karşılamayan bi ses tonu ve bakışla||"
    "Çabuk odana dön||"
    "Bu sana son uyarım||"
),
"layout": "single_focus",
        "images": [ "images/S08.5_DONT_LOOK_HİM"],
        "choices": {
            "1": ("Haddini bildir", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
"S14_PRE_CONFRONT": {
    "layout": "single_focus",
    "text": (
    "Nefesin hızlanıyor||"
    "Zihninde görüntüler parçalanıp birleşiyor.[[BLINK]]□|||"

    "Bir an||"
    "Bir tartışma.[[BLINK]]□|||"

    "-Bunu yapmana izin veremem.[[BLINK]]"
),
    "image": "images/s14_pre_confront.png",

    # ✅ Memory glitch / blur pulse efekti
    "dizzy": {"mode": "blur", "intensity": "strong", "speed_ms": 60},

    "choices": {
        "1": ("kendini topla ve koridora çık", "S04_CORRIDOR7", []),
    },
},


"S16_JANITOR_INFO": {
    "text": (
    "Bir süre susuyor||"
    "Birşey hatırlamıyor musun?.[[BLINK]]□|||"

    "Boşver||"
    "\"Kamera odasına gittin mi?[[BLINK]]\""
),
"layout": "single_focus",
    "images": [
        
        "images/s16_janitor_info_copy.png",
        
    ],
    "choices": {
        "1": ("Evet de (yalan söyle)", "S8.4_ANSWER_HİM3", []),
        "2": ("Hayır de", "S17_JANITOR_REACT", []),
        "3": ("Ayak seslerini sor", "S8.4_ANSWER_HİM4", []),
    },
},
     "S8.4_ANSWER_HİM4": {
        "text": (
    "Ayak sesimi||"
    "Burda tüm gece sadece ben vardım.[[BLINK]]□|||"

    "Belki benim ayak sesimi duymuşsundur||"
    "Merak etme ||"
),
"layout": "single_focus",
        "images": [ "images/S08.5_DONT_LOOK_HİM"],
        "choices": {
            "1": ("Tehtidine karşılık ver", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
    "S8.4_ANSWER_HİM3": {
        "text": (
    "##Pek hoş karşılamayan bi ses tonu ve bakışla||"
    "Bana yalan söylemen hiç hoşuma gitmedi.[[BLINK]]□|||"

    "Az önce ordaydım||"
    "Şimdi çabuk odana dön||"
    "Bu sana son uyarım||"
),
"layout": "single_focus",
        "images": [ "images/S08.5_DONT_LOOK_HİM.png"],
        "choices": {
            "1": ("Tehtidine karşılık ver", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
"S17_JANITOR_REACT": {
    "text": (
    "Gözlerini kısıyor||"
    "Aradığın cevapları orada bulacaksın||"
    "Ama dikkatli ol||"
),
"layout": "single_focus",
    "images": [
        
        "images/s17_janitor_react.png",
        
    ],
    "choices": {
        "1": ("Kafeteryaya kaç", "S8.6_go_to_caffeteria", []),
        "2": ("Kamera odasına git", "S07_CAMERA_DOOR", []),
        "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
    },
},

 
"END_E01": {
    "layout": "single",
    "image": "images/end_e01.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_E01",

    "ending_sequence_cfg": {
        "images": [
            "images/end_e01.png",
        ],
        "holds_ms": [5000],
        "instant_switch": False,
        "fade_in_ms": 1200,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,

        "overlay_text": (
    "Gözlerini kapatırsın||"
    "Ayak sesleri durur||"
    "Saat değişmiyor||"
    "Asla oradan ayrılmazsın||"
),

        # ✅ YAVAŞ & DOĞAL TYPEWRITER
        "overlay_type_ms": 55,        # harf hızı (daha da yavaş istersen 65-75)
        "overlay_seg_pause_ms": 260,  # || sonrası durak
        "overlay_page_pause_ms": 700, # ||| sonrası durak
        "overlay_box_pause_ms": 1200, # □ (kullanırsan)

        "next_scene": "LOBBY",
    },

    "final_screen_line": "02:17.",
    "ending_title": "Erken Son",

    "ending_music": "sounds/ending_theme.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,

    "final_hold_ms": 3000,
    "final_fade_ms": 1800,
    "title_pop_ms": 180,
    "title_pop_steps": 10,
    "title_font": 56,

    "auto_next": "LOBBY",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},


"END_E02": {
    "layout": "single_focus",
    "image": "images/end_e02.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_E02",

    # ✅ FULLSCREEN sequence (tek görsel)
    "ending_sequence_cfg": {
        "images": [
            "images/end_e02.png",
        ],
        "holds_ms": [5000],
        "instant_switch": False,
        "fade_in_ms": 1200,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,

        # ✅ altta yazacak metin (|| tokenlarıyla)
        "overlay_text": (
    "Kıpırdamazsın||"
    "Tik… tak…||"
    "Ayak sesleri yaklaşır||"
    "Bu sefer durmaz||"
),

        # ✅ token duraksamaları (yarım saniye)
        "overlay_seg_pause_ms": 500,
        "overlay_page_pause_ms": 900,
        "overlay_box_pause_ms": 1200,

        "next_scene": "LOBBY",
    },

    "ending_music": "sounds/ending_theme4.mp3",
    "ending_music": "sounds/ending_ticking.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,

    "final_screen_line": "Saat: 02:18.",
    "ending_title": "son yazı",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,

    "auto_next": "LOBBY",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},
"END_E03": {
    "layout": "single_focus",
    "image": "images/end_e03.png",
    "text": "##",

    "ending": True,
    "ending_id": "END_E03",

    "ending_sequence_cfg": {
        "images": [
            "images/end_e03.png",
        ],
        "holds_ms": [5000],
        "instant_switch": False,
        "fade_in_ms": 1200,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,

        "overlay_text": (
    "Böyle bi ortamda karanlıkta kalmak||"
    "Pek de iyi bir fikir değil||"
),

        "overlay_seg_pause_ms": 500,
        "overlay_page_pause_ms": 900,
        "overlay_box_pause_ms": 1200,

        "next_scene": "LOBBY",
    },

    "ending_music": "sounds/ending_theme3.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,

    "final_screen_line": "Saat: 02:18.",
    "ending_title": "Kötü son",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,

    "auto_next": "LOBBY",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},
"END_CAUGHT_WHILE_REALIZING": {
    "layout": "single_focus",
    "image": "images/end_caught.png",
    "text": "##",

    "ending": True,
    "ending_id": "CAUGHT_WHILE_REALIZING",

    "ending_sequence_cfg": {
        "images": [
            "images/end_caught.png",
        ],
        "holds_ms": [6000],
        "instant_switch": False,
        "fade_in_ms": 1200,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,

        "overlay_text": (
    "Kaçmıyorsun||"
    "Bakıyorsun||"
    "Yüz hatları tanıdık… ama nedenini çıkaramıyorsun||"
    "Bu an çok kısa sürüyor||"
    "Bir kol göğsünü sıkıca kavrıyor||"
    "Nefesin kesiliyor||"
    "□Bir süre sonra yatağındasın||"
    "Kolların ve bacakların bağlı||"
    "Oda karanlık||"
    "Saat: 02:17||"
    "Bu sefer kaçmayı denemedin bile||"
),

        "overlay_seg_pause_ms": 500,
        "overlay_page_pause_ms": 900,
        "overlay_box_pause_ms": 2000,  # BLACK2000 hissi için

        "next_scene": "LOBBY",
    },

    "ending_music": "sounds/ending_theme5.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,

    "final_screen_line": "Saat: 02:17.",
    "ending_title": "Tutsak Son",

    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,

    "auto_next": "LOBBY",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},
"S16_CAFETERIA_LISTEN_DUO": {
    "layout": "single",
    "image": "images/s16_cafeteria_check_around2.png",
    "text": (
        "##Kapıya kulak veriyorsunuz||"
        "Ayak sesleri yaklaşıyor gibi||"
        "Burada daha fazla oyalanmak istemiyorsun.[[BLINK]]"
    ),
    "choices": {
        "1": ("Tezgâha yönel", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        "2": ("Saklan", "S16_CAFETERIA_HIDE_DUO", []),
    },
},

"S16_CAFETERIA_LISTEN": {
    "layout": "single",
    "image": "images/s16_cafeteria_solo.png",
    "text": (
        "##Sesin geldiği yöne kulak kesiliyorsun||"
        "Kısa bir sessizlik oluyor||"
        "Burada daha fazla beklemek istemiyorsun.[[BLINK]]"
    ),
    "choices": {
        "1": ("Tezgâhın arkasına bak", "S16_CAFETERIA_CHESS_SETUP", []),
        "2": ("Saklanacak bir yer ara", "S16_CAFETERIA_HIDE", []),
    },
},

"END_E04": {
    "layout": "single_focus",
    "image": "images/end_e03.png",
    "text": "##",
    "ending": True,
    "ending_id": "END_E04",
    "ending_sequence_cfg": {
        "images": [
            "images/end_e03.png"
        ],
        "holds_ms": [5000],
        "instant_switch": False,
        "fade_in_ms": 1200,
        "fade_out_ms": 900,
        "fade_steps": 64,
        "cover": True,
        "overlay_text": (
            "Kaçmak için doğru anı bulamadın||"
            "Döngü seni yeniden içine çekti.||"
        ),
        "overlay_seg_pause_ms": 500,
        "overlay_page_pause_ms": 900,
        "overlay_box_pause_ms": 1200,
        "next_scene": "LOBBY",
    },
    "ending_music": "sounds/ending_theme3.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,
    "final_screen_line": "Saat: 02:17.",
    "ending_title": "Kilitli Son",
    "final_type_ms": 55,
    "final_hold_ms": 2400,
    "final_fade_ms": 1400,
    "title_pop_steps": 10,
    "auto_next": "LOBBY",
    "auto_next_after": True,
    "auto_delay_ms": 0,
    "auto_next_delay_ms": 0,
},

}

STORY = STORY_TR