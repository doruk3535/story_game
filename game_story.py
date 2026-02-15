

# ============================================================
# ENGLISH STORY
# ============================================================

STORY_EN = {}

# ============================================================
# TURKISH STORY (EN ile birebir ID + uzunluk)
# ============================================================

STORY_TR = {

    "S01_START": {
        "text": (
            "##Saat 02:17.||"
            "##Telefon ekranın açık ama bildirim yok.||"
            "##Koridordan düzenli ayak sesleri geliyor.||"
            "Fazla düzenli."
        ),
        "images": [
            "images/s01_1_phone.png",
            "images/s01_2.png",
            "images/s01_3.png",
        ],
        "footstep_on_segment": 2,
        "choices": {
            "1": ("Kapıya yaklaş", "S02_CORRIDOR_ENTRY", []),
            "2": ("Telefonuna bak", "S03_PHONE_LOCK", []),
            "3": ("Uyumaya çalış", "END_E01", []),
        },
    },

    "S02_CORRIDOR_ENTRY": {
        "text": (
            "##Kapının önündesin.||"
            "##Ayak sesleri kapının tam önünde duruyor.||"
            "##Biri seni dinliyor.||"
            "Nefesini bile duyuyorsun."
        ),
        "images": [
            "images/s02_door.png",
            "images/s02_2.png",
            "images/s02_3.png",
        ],
        "choices": {
            "1": ("Kapıyı aç", "S04_CORRIDOR", []),
            "2": ("Kapıyı kilitle", "S09_LOOP_ROOM", []),
            "3": ("Kapının altına bak", "S05_FOOTPRINT", []),
        },
    },

"S03_PHONE_LOCK": {
    "text": (
        "##Kilit ekranına bakıyorsun.||"
        "##Eski bir bildirim var.||"
        "##Bugüne ait değil. Gönderen bilinmiyor.||"
    ),
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
        "##Kurtul oradan. Çabuk.||"
        "Orası artık güvenli değil.||"
        "Kimseye güvenme.||"
    ),
    "images": [
        None,
        "images/s03_5_notification.png",
        None,
    ],
    "choices": {
        "1": ("Koridora çık", "S04_CORRIDOR_After_NOTIFICATION", ["O2"]),
        "2": ("Telefonu kapat", "S09_LOOP_ROOM", []),
        "3": ("Galeriyi aç", "S06_GALLERY", []),
    },
},


    "S04_CORRIDOR": {
        "text": (
            "##Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
        },
    },

    "S04_CORRIDOR_After_NOTİFİCATİON": {
        "text": (
            "##Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },

    "S04_CORRIDOR_after_footprint": {
        "text": (
            "##Ayak izleri ileri uzanıyor||"
            "Koridor sessiz.||"
            "Işıklar hafifçe titriyor.||"
            "ilerde biri var ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki silüete yönel", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },

    "S04_CORRIDOR_AFTER_GALERY": {
        "text": (
            "##Bi saniye .||"
            "Bu koridoru tanıyorum .||"
            "Neden hatırlamıyorum  ."
        ),
        "images": [None, "images/s04_corridor.png", None],
        "flicker": {"index": 2, "slot": "C", "intensity": "strong", "until": "scene_end"},
        "choices": {
            "1": ("Kamera odasına yönel", "S07_CAMERA_DOOR", []),
            "2": ("ilerdeki adama sor", "S08_JANITOR", []),
            "3": ("Odaya geri dön", "S09_LOOP_ROOM_2", []),
        },
    },

    "S04_CORRIDOR_After_camera": {
        "text": (
            "##Koridordasın.||"
            "Boş.||"
            "Az önce biri vardı ama artık yok.||"
            "Ayak sesi yok."
        ),
        "images": [None, "images/s04_corridor_empty.png", None],
        "choices": {
            "1": ("Yangın merdivenine git", "S15_FIRE_EXIT", []),
            "2": ("Yemekhaneye yönel", "S16_CAFETERIA_FROM_CAMERA", []),
            "3": ("Odana geri dön", "S09_LOOP_ROOM_4", []),
        },
    },
"S16_CAFETERIA_FROM_CAMERA": {
    "layout": "single",
    "text": (
        "Yemekhaneye yürüyorsun.||"
        "Kapıyı itiyorsun.||"
        "İçerisi… fazla aydınlık.|||"
        "##Ve girer girmez birini görüyorsun.||"
        "Bu sensin kameralarda gördüğün kişi.||"
        "Neden nasılını soramadan:||"
        "‘Acele et, burdan kurtulmamız gerek.’ diyor.||"
        "‘Bize bi anahtar lazım… yangın çıkışı için.’"
    ),
    "image": "images/s16_cafeteria_from_camera.png",
    "choices": {
        "1": ("Saklan", "S16_CAFETERIA_HIDE", []),
        "2": ("Birlikte hareket et", "S16_CAFETERIA_CHECK_AROUND", []),
        "3": ("Tek başına hareket et", "S16_CAFETERIA_SOLO", []),
    },
},


"S16_CAFETERIA_CHECK_AROUND": {
    "text": (
        "##Etrafına bakıyorsun.||"
        "Masalar düzenli.||"
        "Sessizlik fazla temiz.|||"
        "Kapının altından hafif bir gölge kayıyor.||"
        "ORTANCA: \"Geldi…\""
    ),
    "choices": {
        "1": ("Tezgâha yönel", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        "2": ("Saklan", "S16_CAFETERIA_HIDE_DUO", []),
        "3": ("Kapıya kulak ver", "S16_CAFETERIA_LISTEN_DUO", []),
    },
},
"S16_CAFETERIA_CHECK_AROUND2": {
    "text": (
        "##Çabuk.||"
        "Benimle gel.||"
      
    ),
    "choices": {
        "1": ("Tezgâha yönel", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        "2": ("Saklan", "S16_CAFETERIA_HIDE_DUO", []),

    },
},




"S16_CAFETERIA_CHESS_SETUP_DUO": {
    "text": (
        "##Tezgâhın arkasına geçiyorsunuz .||"
        "Burası çalışanlara ait gibi duruyor.||"
        "Çekmeceler düzenli, ama biri denense şifreyle kilitlenmiş .|||"
        "Çekmeceyi zorluyorsun ama açılmıyor .||"
        "Etrafı incelediğnde iki şey görüyorsun .||"
        "Bir satranç tahtası.||"
        "Ve bir yangın tüpü:||"
        "Ne yapmalıyım”||"
    ),
    "choices": {
        "1": ("Satranç tahtasını incele", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın tüpüyle \n kilidi kırmaya çalış", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_CHESS_PUZZLE_SCREEN_DUO": {
    
    "images": [None, "images/s16_chess_puzzle_screen.png", None],
    "text": (
        "Tahtaya bakıyorsun.||"
        "Taşlar sana bir şey ima ediyor.|||"
        "Oyun sonu çok yakın gibi.||"
        "Taşların koordinatları sana bir şeyler anlatıyor.|||"
        "Şifre bu olabilir mi?||"
        "Ama hangi taş ve hangi koordinat?|||"
        "Biraz düşündükten sonra fark ediyorsun:||"
        "BULDUM! Tek hamlede mat var.|||"
        "ŞİFRE BU OLMALI."
    ),
    "choices": {
        "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A_DUO", []),
        "2": ("At g6'ya oynar", "S16_CHESS_TRY_B_DUO", []),
        "3": ("At f7'ye oynar", "S16_CHESS_TRY_C_DUO", []),
    },
},

"S16_UNLOCK_SEQUENCE_DUO": {
    "text": (
        "Tezgâhın altına eğiliyorsun.||"
        " şifreli olan kilidi şifreni girmeye hazırlanıyorsun.||"
    ),
    "images": [None, "images/s16_1_counter_back.png", None],
    "choices": {
        "1": ("h7 ", "S16_kilit_açılmıyor_DUO", []),
        "2": ("g6", "S16_şifre_doğru_DUO", []),
        "3": ("f7", "S16_kilit_açılmıyor_DUO", []),
    },
},
"S16_şifre_doğru_DUO": {
    "text": (
        "Biliyordum.||"
        "Kilit açıldı.||"
        "İçinde bir anahtar var.||"
    ),"images": [None, "images/s16_sifre_dogru.png", None],

    "choices": {
        "1": ("Anahtarı al", "S16_KEY_TAKEN_DUO", ["I_KEY"]),
    },
},
"S16_KEY_TAKEN_DUO": {
    "text": (
        "Anahtarı aldın.||"
        "Ne açtığını bilmiyorsunuz .|||"
        "Gelecekteki halinle yanına geliyor .||"
        "G: \"Tamam.||"
        "Yangın çıkışı.\"|||"
        "Yan taraftaki kapıdan bir ses geliyor.||"
        "Hafif bir tıkırtı.||"
        "Sanki biri kapının arkasında biri var .|||"
        "Kafeterya koridoru ise bomboş.||"
        "Işıklar titriyor.|||"
        "ORTANCA fısıldıyor: \"Düşünme.||"
        "Ya şimdi… ya hiç.\""
    ),
    "choices": {
        "1": ("Yangın çıkışına birlikte koş", "S17_DUO_ESCAPE_RUN", []),
        "2": ("Ses gelen kapıya yaklaş", "S16_DUO_CHECK_SOUND", []),
        "3": ("Geri çekil ve saklan", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S17_DUO_ESCAPE_RUN": {
    "text": (
        "Anahtarı avucunda sıkıyorsun.||"
        "Ortanca halin yanında.|||"
        "ORTANCA: \"Şimdi.\"|||"
        "İkiniz birden koridora fırlıyorsunuz.||"
        "Ayak sesleriniz aynı ritimde büyüyor.|||"
        "Işıklar titriyor.||"
        "Sanki her titreme başka bir saniyeyi yutuyor.|||"
        "Yangın çıkışı tabelası beliriyor.|||"
        "Kapıya vardığında anahtarı kilide sokuyorsun.||"
        "Elin titriyor… ama çeviriyorsun.|||"
        "Tık.|||"
        "Kapı açılıyor ve—|||"
        "Bir koridor değil.||"
        "Bir boşluk.|||"
        "Kapının içi kıvrılıyor.||"
        "Işık değil… zaman dönüyor.|||"
        "Bir ZAMAN PORTALI.|||"
        "Arkanızdan bir ses:|||"
        "\"DUR!\"|||"
        "Hademe görünüyor.||"
        "Yaşlı… yorgun… ama gözleri saplantılı.|||"
        "Koşamıyor.||"
        "Ama sesi yetiyor.|||"
        "\"Bir adım daha atarsanız… her şey tekrar parçalanır.\"|||"
        "ORTANCA dişlerini sıkıyor: \"Yalan söylüyor.\"|||"
        "Hademe başını sallıyor.|||"
        "\"Ben… hepinizi biliyorum.\"|||"
        "\"Çünkü ben de sizim.\"|||"
        "Bir an sessizlik.||"
        "Portalın içi dalgalanıyor.|||"
        "Hademe konuşmaya başlıyor:|||"
        "\"Ben bu döngüyü başlatan kişiyim.\"|||"
        "\"Karımı ve kızımı kaybettim… ve bunu kabullenemedim.\"|||"
        "\"Zamanla oynadım.||"
        "Bir kapı yaptım.||"
        "O günün öncesine… o kazanın öncesine.\"|||"
        "\"Onları kurtardım.\"|||"
        "\"Sonra zaman… bedelini istedi.\"|||"
        "\"Bir yarık açıldı.||"
        "Milyarlarca hayat, geçmiş ve gelecek üst üste bindi.\"|||"
        "\"Düzeltmek için geri geldim… ama çok geç kaldım.\"|||"
        "\"Genç halim beni dinlemedi.||"
        "Ortanca halim kaçmayı seçti.||"
        "Ve en sonunda… bu bina 02:17’de kilitlendi.\"|||"
        "\"Siz…\"|||"
        "Parmağıyla sizi işaret ediyor.|||"
        "\"Siz bu anomaliyi sabit tutuyorsunuz.\"|||"
        "\"Biri kalırsa zaman dengelenir.||"
        "Hepiniz giderseniz… yarık büyür.\"|||"
        "ORTANCA: \"Bizi korkutmaya çalışma!\"|||"
        "Hademe boğuk bir nefes alıyor.|||"
        "\"Korkutmuyorum.\"|||"
        "\"Sadece ilk defa… seçimi doğru yapın istiyorum.\"|||"
        "Portalın uğultusu yükseliyor.|||"
        "Bir saniyen var.||"
        "Ya bir kader… ya bir kaçış."
    ),
    "choices": {
        "1": ("Ortanca halinle kaç", "END_DUO_ESCAPE_TWO_LEAVE", []),
        "2": ("Ortanca halini gönder, sen kal", "END_DUO_STAY_SOLO_SACRIFICE", []),
        "3": ("Hepimiz beraber kaçalım", "END_DUO_ESCAPE_ALL_THREE", []),
    },
},

"END_DUO_ESCAPE_TWO_LEAVE": {
    "text": (
        "Ortanca halin bileğini yakalıyorsun.|||"
        "Sen: \"Koş.\"|||"
        "ORTANCA bir an tereddüt ediyor.||"
        "Sonra gözlerini kısıyor: \"Tamam.\"|||"
        "İkiniz birden portala hamle ediyorsunuz.|||"
        "Hademe arkanızdan bağırıyor:|||"
        "\"YAPMAYIN!\"|||"
        "\"Bu bir son değil…\"|||"
        "\"Bu bir kırılma!\"|||"
        "Ama artık duymuyorsun.|||"
        "Portalın içi sizi yutuyor.|||"
        "Kulakların uğulduyor.||"
        "Gözlerin yanıyor.|||"
        "Bir an… dünyanın üst üste bindiğini görüyorsun.|||"
        "Koridor.||"
        "Kafeterya.||"
        "Oda.||"
        "Ve 02:17.|||"
        "Sonra—|||"
        "Yatak.|||"
        "Tavan.|||"
        "Telefon ekranı.|||"
        "Saat: 02:18.|||"
        "Ortanca halin yanında nefes nefese.|||"
        "ORTANCA fısıldıyor: \"Başardık mı?\"|||"
        "Cevap veremiyorsun.||"
        "Çünkü telefonuna bir bildirim düşüyor.|||"
        "Gönderen: Bilinmiyor.|||"
        "Mesaj: \"İkiniz çıktınız…||"
        "Ama yarık da çıktı.\""
    ),
    "ending_id": "END_DUO_ESCAPE_TWO_LEAVE",
},

"END_DUO_STAY_SOLO_SACRIFICE": {
    "text": (
        "Ortanca haline bakıyorsun.|||"
        "Sen: \"Git.\"|||"
        "ORTANCA: \"Ne? Hayır—\"|||"
        "Sen: \"Dinle.||"
        "Eğer biri kalacaksa… o ben olayım.\"|||"
        "ORTANCA gözleri dolu dolu: \"Saçmalama.\"|||"
        "Sen anahtarı onun avucuna itiyorsun.|||"
        "Sen: \"Koş.||"
        "Yaşamak zorundasın.\"|||"
        "ORTANCA: \"Seni bırakamam.\"|||"
        "Hademe sessizce izliyor.|||"
        "\"Bu…\" diyor, \"zamanın istediği şey.\"|||"
        "Ortanca halin dişlerini sıkıyor.|||"
        "Son bir kez sana bakıyor.|||"
        "Ve portala atlıyor.|||"
        "Portalın ışığı yüzünü yalıyor… sonra uzaklaşıyor.|||"
        "Kapı hala açık.||"
        "Ama artık rüzgar gibi soğuk.|||"
        "Hademe ağır ağır yaklaşıyor.|||"
        "\"Şimdi anladın,\" diyor.|||"
        "Sen kapıyı kapatıyorsun.|||"
        "Tık.|||"
        "Kilit.|||"
        "Saatin sesi geri geliyor.|||"
        "Tik… tak…|||"
        "Duvardaki saate bakıyorsun:|||"
        "02:17.|||"
        "Ve bu sefer…|"
        "Zaman ilerlemiyor.|||"
        "Ama en azından biliyorsun.|||"
        "Bu senin seçimin."
    ),
    "ending_id": "END_DUO_STAY_SOLO_SACRIFICE",
},

"END_DUO_ESCAPE_ALL_THREE": {
                            
    "text": (
        "Sen hademeye bakıyorsun.|||"
        "Sen: \"Madem hepimiz aynıyız…||"
        "o zaman birlikte bitirelim.\"|||"
        "ORTANCA: \"Ne yapıyorsun?\"|||"
        "Sen: \"Onu da götürelim.\"|||"
        "Hademe ilk defa gerçekten sarsılıyor.|||"
        "\"Ben…\" diyor.||"
        "\"Ben bunu hak etmiyorum.\"|||"
        "Sen bir adım yaklaşıyorsun.|||"
        "Sen: \"Belki de mesele hak etmek değil.||"
        "Mesele… bitirmek.\"|||"
        "ORTANCA nefes alıyor.|||"
        "Sonra başını sallıyor: \"Tamam.\"|||"
        "Üçünüz aynı anda portala yaklaşıyorsunuz.|||"
        "Portal çılgın gibi dalgalanıyor.|||"
        "Sanki kararınız onu rahatsız etmiş gibi.|||"
        "Hademe fısıldıyor:|||"
        "\"Eğer gidersem… zaman tutunacak bir şey bulamayacak.\"|||"
        "Sen: \"O zaman…||"
        "ya özgür olur… ya yıkılır.\"|||"
        "Üçünüz birden atlıyorsunuz.|||"
        "Bir an… her şey sessizleşiyor.|||"
        "Sonra dünya katlanıyor.|||"
        "Renkler yok.||"
        "Sesler yok.|||"
        "Sadece bir sayı:|||"
        "02:17|||"
        "…ve ardından…|||"
        "02:18.|||"
        "Gözlerini açıyorsun.|||"
        "Yatak.||"
        "Tavan.|||"
        "Ortanca halin yanında.|||"
        "Ve hademe… yok.|||"
        "Telefonun ekranı yanıyor.|||"
        "Bir bildirim:|||"
        "\"Zaman serbest.|||"
        "Ama artık koruyan yok.\"|||"
        "Dışarıdan bir siren sesi geliyor.|||"
        "Uzakta… bir şeyler yanıyormuş gibi."
    ),
    "ending_id": "END_DUO_ESCAPE_ALL_THREE",
},

"S16_DUO_CHECK_SOUND": {
    "text": (
        "Sesin geldiği kapıya yaklaşıyorsun.||"
        "Gelcekteki halin hemen arkanda.|||"
        "G: \"Yapma…\"|||"
        "Ama çok geç.||"
        "Tıkırtı bir anda kesiliyor.|||"
        "Kafeteryadaki ışıklar bir an… yanıp sönmeye başlıyor.|||"
        "İkiniz de aynı anda arkanızı dönüyorsunuz.|||"
        "Koridorun ucunda bir gölge.||"
        "Hademe.|||"
        "Bu sefer koşmuyor.||"
        "Sakin bi şekilde üzerinize geliyor.|||"
        "G:Şimdi hapı yuttuk \"Bizi gördü.\"|||"
        "Bir adım geri çekiliyorsun—|||"
        "Ama bileğin bir anda kavranıyor.|||"
        "Güçlü.||"
        "Soğuk.||"
        "Kesin."
    ),
   "choices": {
        "1": ("", "S15_CAFETERIA_STORAGE_DUO" ,[]),
        "2": ("Devam", "S15_CAFETERIA_STORAGE_DUO", []),
        "3": ("", "S15_CAFETERIA_STORAGE_DUO",[]),
    },
},

"S16_CHESS_TRY_A_DUO": {
    "images": [None, "images/s16_chess_try_a.png", None],
    "text": (
        "Kale h7 gibi ama emin değilim .||"
        "Ozaman şifre h7 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"
    ),
    "choices": {
        "1": ("Şifreyi deneyelim bakalım", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},

"S16_CHESS_TRY_B_DUO": {
    "images": [None, "images/s16_chess_try_b.png", None],
    "text": (
        "Atı g6'ya oynuyorsun.||"
        "Ozaman şifre g6 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"
    ),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},

"S16_CHESS_TRY_C_DUO": {
    "images": [None, "images/s16_chess_try_c.png", None],
    "text": (
        "Atı f7'ya oynuyorsun.||"
        "Ozaman şifre f7 olabilirmi.||"
        "Denemekten zarar gelmez herhalde:||"
    ),
    "choices": {
        "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE_DUO", []),
        "2": ("Yangın tüpüne al", "S16_yangın_tüpü", []),
        "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_kilit_açılmıyor_DUO_A": {
    "text": (
        "Yanlış hesaplamış olmalıyım.||"
        "Bidaha denemeliyim .||"
    ),
    "images": [None, "images/s16_kilit_acilmiyor_duo_a.png", None],

    "choices": {
        "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın söndürücüyü al", "S16_şifre_doğru_DUO", []),
        "3": ("SAKLAN !!!", "S16_CAFETERIA_HIDE_DUO", []),
    },
},
"S16_kilit_açılmıyor_DUO_C": {
    "text": (
        "Yanlış hesaplamış olmalıyım.||"
        "Bidaha denemeliyim .||"
    ),
    "images": [None, "images/s16_kilit_acilmiyor_duo_a.png", None],

    "choices": {
        "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_DUO", []),
        "2": ("Yangın söndürücüyü al", "S16_şifre_doğru_DUO", []),
        "3": ("SAKLAN !!!", "S16_CAFETERIA_HIDE_DUO", []),
    },
},

    "S16_CAFETERIA_HIDE_DUO": {
        "text": (
            "Tezgâhın altına giriyorsunuz.|| Dizleriniz taş zemine gömülüyor.||"
            "Kapı açılıyor.|||"
            "Hademe: 'Nerdesiniz... orada olduğunuz u biliyorum.'|||"
            "Ayakkabısının sesi... duruyor. Tam önünde."
        ),
        "choices": {
            "1": ("Sessiz kal / nefesini tut", "S15_HIDE_SILENT_1_DUO", ["F_HIDE"]),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
            "3": ("Etrafı Aaramya başlayın.'", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        },
    },
    # Alias: Akış değişmesin diye S15_FIRE_EXIT'ı kilitli sahneye yönlendiriyoruz
"S15_FIRE_EXIT": {
    "text": (
        "##Yangın kapısının önündesin.||"
        "Kolu indiriyorsun.||"
        "Kımıldamıyor.||"
        "Kilitli.||"
    ),
    "images": [
        None,
        "images/s15_fire_exit.png",
        None,
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
            "Yerde bir ayakkabı izi.||"
            "Nedense çok tanıdık."
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
            "##Fotoğrafını çektin ve bakmak için galeriyi açtın ||"
            "##Galerinde eski fotoğraflar var.||"
            "Çoğunu hatırlamıyorsun.||"
            "Ama biri öne çıkıyor:||"
            "##Koridor,"
            "Gece,"
            "Ve sen."
        ),
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
            "##Galerinde eski fotoğraflar var.||"
            "##Çoğunu hatırlamıyorsun.||"
            "Ama biri öne çıkıyor:||"
            "##Koridor,"
            "Gece,"
            "Ve sen."
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
            "##Kamera odasının kapısındasın.||"
            "İçeriden hafif bir uğultu geliyor.||"
            "Kapı açık ."
        ),
        "images": [None, "images/s07_camera_door.png", None],
        "choices": {
            "1": ("Kapıyı aç", "S11_CAMERA_ROOM", ["O1"]),
            "2": ("içeriyi dinle", "S12_CAMERA_HINT", []),
            "3": ("koridora geri dön", "S04_CORRIDOR_After_camera", []),
        },
    },

    "S08_JANITOR": {
        "text": (
            "##Temizlik arabasının yanında biri duruyor.||"
            "##Gece temizlikçisi.||"
            "##Seni görünce kaşlarını çatıyor.||"
            "Sanki seni tanıyor."
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
            "##Sana baktı ve dediki.||"
            "Bu saatte koridorda gezmenin ||"
            "Yasak olduğunu bilmiyormusun .||"
        ),
        "images": [None, "images/S08.5_DONT_LOOK_HİM.png", None],
        "choices": {
            "1": ("Tersle", "S8.4_ANSWER_HİM", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },

    "S8.4_ANSWER_HİM": {
        "text": (
            "##Sen kendi işine bak.||"
            "Bunu pek hoş karşılamyan bi ses tonu ve bakışla.||"
            "'Çabuk odana dön' dedi .||"
        ),
        "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
        "choices": {
            "1": ("Haddini bildir", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },

"S8.6_go_to_caffeteria": {
    "text": (
        "##Bir anda koşmaya başlıyorsun.||"
        "##Adımların koridorda yankılanıyor.||"
        "Işıklar uzuyor, daralıyor.||"
        "##Tam önünde duruyor Kafeterya.||"

    ),
    "images": [
        "images/s08_6_collision.png",
        "images/s08_6_2.png",
        "images/s08_6_3.png",
    ],

 "choices": {


            


        "2": ("Kafeteryaya gir", "S8.7_CAFETERIA_KARSILASMA", []),


    },
},
"S8.7_CAFETERIA_KARSILASMA": {
    "text": (
        "##İçerde birine çarpıyorsun .||"
        "Çarpmanın etkisiyle yere düşüyo.||"
        "##Dur bi saniye sende kimsin.||"
        "Ve Neden.||"
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
        "##Tek başına ilerlemeyi kafaya koymuşsun.||"
        "Işıklar açık.||"
        "Masa ve sandalyeler düzgün.|||"
        "Her şey fazla normal.||"
        "Kapıyı arkandan kapatıyorsun.||"
        "Kapıyı kapattığın anda .|||"
        "Kapının arkasındaki boğuşma seslerini duyuyorsun.||"
        "Birkaç saniye sonra.|||"
        "Sonra kesiliyor.||"
        "Sessizlik geri geliyor.||"
        "Bununla unutup yoluna bakman gerek."
    ),
    "choices": {
        "1": ("Tezgâhın arkasına bak", "S16_CAFETERIA_CHESS_SETUP", []),
        "2": ("Saklanacak bir yer ara", "S16_CAFETERIA_HIDE", []),
        "3": ("Sesin geldiği yöne kulak kesil", "S16_CAFETERIA_LISTEN", []),
    },
},

"S16_CAFETERIA_CHESS_SETUP": {
    "text": (
        "##Tezgâhın arkasına geçiyorsun.||"
        "Burası çalışanlara ait gibi duruyor.||"
        "Çekmeceler düzenli, ama biri denense şifreyle kilitlenmiş .|||"
        "Çekmeceyi zorluyorsun ama açılmıyor .||"
        "Etrafı incelediğinde iki şey görüyorsun .||"
        "##Bir satranç tahtası.||"
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
            "Tezgâhın altına giriyorsun.|| Dizlerin taş zemine gömülüyor.||"
            "Kapı açılıyor.|||"
            "Hademe: 'Nerdesin... orada olduğunu biliyorum.'|||"
            "Ayakkabısının sesi... duruyor. Tam önünde."
            
        ),"images": [None, "images/s16_cafeteria_hide.png", None],

        "choices": {
            "1": ("Sessiz kal / nefesini tut", "S15_HIDE_SILENT_1", ["F_HIDE"]),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
            "3": ("Etrafı Aramya başla.", "S16_CAFETERIA_CHESS_SETUP", []),
        },
    },

    "S15_HIDE_SILENT_1": {
        "text": (
            "Nefesini kesiyorsun. Göğsün yanıyor.||"
            "Hademe kıpırdamıyor. Sanki dinlemiyor... sanki zaten biliyor.||"
            "Fısıltı gibi: 'Bu kadar sessizlik... hep aynı.'"
        ),
        "choices": {
            "1": ("Sessiz kal / kıpırdama", "S15_HIDE_SILENT_2", []),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
        },
    },
    "S15_HIDE_SILENT_1_DUO": {
        "text": (
            "Nefesini kesiyorsun. Göğsün yanıyor.||"
            "Hademe kıpırdamıyor. Sanki dinlemiyor... sanki zaten biliyor.||"
            "Fısıltı gibi: 'Bu kadar sessizlik... hep aynı.'"
        ),
        "choices": {
            "1": ("Sessiz kal / kıpırdama", "S15_HIDE_SILENT_2_DUO", []),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        },
    },
    "S15_HIDE_SILENT_2": {
        "text": (
            "Parmakların istemsiz titriyor ama durduruyorsun.||"
            "Ayakkabı sesi bir adım sağa kayıyor... sonra geri geliyor.||"
            "Hademe: 'Beni oyalama. Zaman bunu sevmez.'"
        ),
        "choices": {
            "1": ("Sessiz kal / dayan", "S15_HIDE_FORCED", []),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
        },
    },
    "S15_HIDE_SILENT_2_DUO": {
        "text": (
            "Parmakların istemsiz titriyor ama durduruyorsun.||"
            "Ayakkabı sesi bir adım sağa kayıyor... sonra geri geliyor.||"
            "Hademe: 'Beni oyalamayın. Zaman bunu sevmez.'"
        ),
        "choices": {
            "1": ("Sessiz kal / dayan", "S15_HIDE_FORCED_DUO", []),
            "2": ("Ses çıkar (tıkırtı)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        },
    },
    "S15_HIDE_FORCED": {
        "text": (
            "Sessizliğin içine batıyorsun. Bu artık saklanmak değil.||"
            "Hademe tam önünde duruyor. Eğilmiyor.||"
            "Sadece başını yana eğiyor: .'|||"
            "Saklanarak buradan çıkamayacağını anlıyorsun."
        ),
        "choices": {
            "2": ("dikkati başka yöne çek  (sesle)", "S15_HIDE_DISTRACT", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP", []),
        },
    },

    "S15_HIDE_FORCED_DUO": {
        "text": (
            "Sessizliğin içine batıyorsun. Bu artık saklanmak değil.||"
            "Hademe tam önünde duruyor. Eğilmiyor.||"
            "Sadece başını yana eğiyor: .'|||"
            "Saklanarak buradan çıkamayacağını anlıyorsun."
        ),
        "choices": {
            "2": ("dikkati başka yöne çek  (sesle)", "S15_HIDE_DISTRACT_DUO", ["F_NOISE"]),
            "3": ("Etrafı aramaya başla", "S16_CAFETERIA_CHESS_SETUP_DUO", []),
        },
    },

    "S15_HIDE_DISTRACT": {
        "text": (
            "Etrafta bulduğun metal bi şişeyi fırlatttın... küçük ama yeterli.||"
            "Hademe başını aniden çeviriyor.||"
            "'Güzel... sonunda bir kaçmak için bi fırsat.|||'"
            "Tam zamanı bi anda fırlıyosun.||"
            "Ama hademe bunu farkediyiyo.'|||"
            "Olabildiğinde hızlı kafeteryanın kapısından kaçmaya çalışıyosun.||"
            "Ama hademe bunu düşünmüş ve kapıyı kitlemiş.||"
            "Sen daha ne olduğnun bile anlamadan arkanı döndüğün anda seni yakalıyo.||"
        ),
        "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
        "auto_delay_ms": 500,
    },
    "S15_HIDE_DISTRACT_DUO": {
        "text": (
            "Etrafta bulduğun metal bi şişeyi fırlatttın... küçük ama yeterli.||"
            "Hademe başını aniden çeviriyor.||"
            "'Güzel... sonunda bir kaçmak için bi fırsat.|||'"
            "Tam zamanı bi anda fırlıyosun.||"
            "Ama hademe bunu farkediyiyo.'|||"
            "Olabildiğinde hızlı kafeteryanın kapısından kaçmaya çalışıyosun.||"
            "Ama hademe bunu düşünmüş ve kapıyı kitlemiş.||"
            "Sen daha ne olduğnun bile anlamadan arkanı döndüğün anda seni yakalıyo.||"
        ),
        "auto_next": "S15_CAFETERIA_STORAGE_DUO",
        "auto_delay_ms": 500,
    },
    
    "S15_CAFETERIA_STORAGE_DUO": {
        "text": (
            "Depoya atılıyorsunuz. Kapı arkandan tek hamlede kapanıyor.||"
            "Kilit sesi… kapıyı üstüne kapatıyor.|||"
            'Kendinle başbaşa konuşmaya başlıyorsun'
            "ORTANCA: \"o hademede sanada garip gelen bişey yokmu.\"|||"
            "ORTANCA: \"Tanıdık bişey.\"|||"
            "Sen: \"Dur tahmin ediyim ?\"||"
            "ORTANCA: \"evet... doğru tahmin ettin .\"||"
            "ORTANCA: \"hepimiz aslında aynı kişiyiz farklı zamanlardan.\"||"
            "ORTANCA: \"seni uyarmaya gelmiştim \"|||"
            "Sen: \"Peki bu nasıl oluyor neden 3 farklı zaman birbiri içinde\"||"
            "ORTANCA: \"O kadarını bilmiyorum .\"|||"
            "ORTANCA: \"tek bildiğim seni burda tutmak istiyo .\"|||"
            "ORTANCA: \"Ve benim seni burda çıkarmam gerek .\"|||"
            "Sen: \"Ama bunu nasıl yapıcaz.\"||"
        ),
        "choices": {
            "1": ("Havalandırmayı kullan(tek başına kurtul odadan)", "S15_RAY_VENT_ESCAPE_SOLO", []),
            "2": ("Hademeye seslen", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
            "3": ("Sessiz kal", "S15_STORAGE_LISTEN", []),
        },
    },
    
    "S15_CAFETERIA_STORAGE_LOCK": {
        "text": (
            "Deponun kapısına kulağının dayadın.||"
            "İçerden bi ses geliyo .|||"
            'Tanıdık bi ses'
            'Anahtar kapının üzerinde'
           
        ),
        "choices": {
            "1": ("Tek başına yangın çıkışına git", "END_SOLO_ESCAPE_A", []),
            "2": ("Kapıyı aç", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
            "3": ("Sessiz kal", "S15_STORAGE_LISTEN", []),
        },
    },
        "S15_CAFETERIA_STORAGE_LOCK": {
        "text": (
            "Deponun kapısına kulağının dayadın.||"
            "İçerden bi ses geliyo .|||"
            'Tanıdık bi ses'
            'Anahtar kapının üzerinde'
           
        ),
        "choices": {
            "1": ("Tek başına yangın çıkışına git", "END_SOLO_ESCAPE_A", []),
            "2": ("Kapıyı aç", "S15_CAFETERIA_STORAGE_LOCK2", []),
           
        },
    },
         "S15_CAFETERIA_STORAGE_LOCK": {
        "text": (
            "Deponun kapısını açtığın anda.||"
            "Arkandan gelen yaşlı adam seni içeri atıp kapıyı üstüne gitliyor.|||"
            'Sanki bunu yapıcağını biliyordu||'
            'Hep orda bekliyordu|||'
            'Sende kimsin ve neden burdasın'
            ''
           
        ),
        "choices": {
            "1": ("Tek başına yangın çıkışına git", "END_SOLO_ESCAPE_A", []),
            "2": ("Kapıyı aç", "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR", []),
           
        },
    },
    "S17_ESCAPE_TOGETHER_OVERCOME_JANITOR": {
        "text": (
            "ORTANCA: \"Tamam. Dinle.\"|||"
            "ORTANCA: \"Onu yenemeyiz.||"
            "Ama onu kandirabiliriz.\"|||"
            "Sen: \"Nasıl?\"|||"
            "ORTANCA: Bilmiyiyorum|||"
            "ORTANCA: Onunla konuşmalıyız.||"
            "Kapıyı tıklatıyorsun.\"|||"
            "Tak.|||"
            "Tak.|||"
            "Tak.|||"
            "Hademe Kapıyı açıyor |||"
            "Hademe:ne istiyorsunuz\"||"
            "ORTANCA: \"anlaşma yapmak istiyoruz.\"|||"
            "Hademe:Neden size güveniyim.||"
            "ORTANCA :Bizi sonsuza kadar burda tutamazsın.|||"
            "Hademe: Aslında yapabilirim |||"
            "ORTANCA :Hayır yapamazsınn aynı zamanda 3 farklı varyantın bulunamsın risklerini biliyosun .||"
            "Hademe:P ekalaNe istiyorsunuz.|||"
            "ORTANCA :ne istediğimi biliyosun.||"
            "ORTANCA :çocuğun burdan gitmesi.||"
            "Hademe:Bunun olmucağını biliyosun .||"
            "Hademe:Neden olamıcağınıda .||"
            "Sen'burda neler oluyo:.||"
            "ORTANCA :Anlat ona.||"
            "Hademe:Pekİ.||"
            "Hademe:Ama bunun hoşuna gidiceğini sanmıyorum .||"
            "Hademe:Şuan geçmiş ve gelecek senin burda kalmana bağlı"
            "Hademe:Sen bi anomalisin zamanı bir arada tutuyorsun "
            "Sen:peki neden ben "
            "Hademe:Çünkü hepsi benim hatam "
            "Hademe:Ve sen bensin "
            "Hademe:Burdan çıkmıyorsun "
            "Deyip kapıyı üzerine kapıyı kapatmak için arkasını dönüyor çıkmaya hazırlanıyor "
        ),
        "choices": {
            "1": ("İtiraz et", "S18_ARGUE_WITH_JANITOR", []),
            "2": ("Hademeye saldır", "S18_ATTACK_JANITOR", []),
            "3": ("Orada kalmaya karar ver", "S18_DECIDE_STAY", []),
        },
    },

    "S18_ARGUE_WITH_JANITOR": {
        "text": (
            "Sen: \"Hayır.\"|||"
            "Sen: \"Bu benim hayatım değil.\"|||"
            "Hademe gözlerini kısıyor…||"
            "Başka çaren yok"
            "Duvardaki saate bakıyorsun 02:17"
            "02:17"
            "ve hep 02:17"
            "Zamanda sıkışıp kaldın"
            "En azından yanlız değilsin"
        ),
        "ending_id": "END_LOCKED_FOR_TIME",
    },

    "S18_DECIDE_STAY": {
        "text": (
            "Sen: yapabilceğimiz bişey yok.\"|||"
            "Sen:  fazla güçlü.\"|||"
            "Hademe gözlerini kısıyor…||"
            "Bende öyle düşünmüştüm"
            "Duvardaki saate bakıyorsun 02:17"
            "02:17"
            "ve hep 02:17"
            "Zamanda sıkışıp kaldın"
            "En azından yanlız değilsin"
        ),
        "ending_id": "END_LOCKED_FOR_TIME",
    },

    "S18_ATTACK_JANITOR": {
        "text": (
            "Sen: \"Hayır.\"|||"
            "Sen: \"Bu benim hayatım değil.\"|||"
            "Böyle bitemez deyip saldırıyorsun…||"
            "Seni geçen seferki gibi kolayca itiyor||"
            "Ama busefer yanlız değilsin ||"
            "Senin ittiği esnada arkandan genç halin gelip|| onu itiyor ve adam yalpalayıp yere düşüyor|||"
            "Bu ikiniz içinde bir fırsat hemen koridora koşuyorsunuz"
            "Yangın çıkışına doğru koşuyorsunuz"
            "Çıkışa vardığında cebinden anahtarı çıkartıp kilide takıyorsun"
            "Yangın çıkışının kapısı açıldığında bi zaman portalı çıkıyor"
            "O sırada yalpalıyan hademe ayağı kalkıyor ve belindeki silahı çıkarıyor"
            "Ve bi el havaya ateş ediyor"
            "ÇABUK DURUN !!!!"
            "Beni buna mecbur bırakmayın"
            "Silahı sana doğru doğrultuyor.|||"
            "O an genç halinin de belinde bir silah olduğunu fark ediyorsun.|||"
            "Genç halin sana bakıyor.||"
            "Sanki kararını senden bekliyor.|||"
            "Portalın içi dalgalanıyor.||"
            "Bir saniyen var."
        ),
        "choices": {
            "1": ("Genç halini tut ve portala atla", "END_ATTACK_PORTAL_JUMP", []),
            "2": ("Silahı indir ve teslim ol", "END_ATTACK_SURRENDER", []),
            "3": ("Hademeyi durdurmaya çalış", "END_ATTACK_DISARM_ATTEMPT", []),
        },
    },

    "END_ATTACK_PORTAL_JUMP": {
        "text": (
            "Genç halinin bileğini yakalıyorsun.|||"
            "Sen: \"ŞİMDİ!\"|||"
            "O seni anlıyor.||"
            "Bir an bile tereddüt etmiyor.|||"
            "İkiniz birden portala atlamak içiçn hamle ediyorsunuz.|||"
            "Hademe bunun olmasına izin veremem deyip ateş ediyor.|||"
            "Elinle karnını tutuyorsun"
            "Heryer kan olmuş"
            "Aynı anda hepiniz karnınızı tutuyorsunuz"
            "Sen ölünce gelecekti varyantlarında ölüyo"
            "Neden yaptın diye soruyorsun son nefesinsle"
            "oda son nefesiyle cevap veriyor"
            "Mecburdum..."
        ),
        "ending_id": "END_ATTACK_PORTAL_JUMP",
    },

    "END_ATTACK_SURRENDER": {
        "text": (
            "Genç halin sana bakıyor.||"
            "Gözleri ‘soru’ değil… ‘öfke’.|||"
            "Sen bir adım öne çıkıyorsun.|||"
            "Sen: \"Yapma.\"|||"
            "Genç halin:Napıyorsun teslim olamazsın"
            "Sen: biz bu değiliz biz katil değiliz"
            "Genç halin: seni dinlemiyor ve silahına davranırken"
            "Genç halin vururluyor"
            "Ve karnını tutmaya başlıyor "
            "Aynı anda yaşlı halinde karnını tutuyor"
            "Genç halin olmadan yaşlı halin olamaz"
            "Genç halininin suratında tatlı bi tebessüm"
            "Sen:bunun olucağını biliyordun değilmi"
            "Son nefesiyle özgür olmanı istedim "
            "artık öözgürsün kendini ve geleceğini kurtar"
            "gözlerini yumuyor"
            "Onun ölümünün anlanlandırman gerek"
            "herşeye rağmen portal giriyorusun "
            "Ardına bakmadan "
            "Portaldan geçtikten sonra"
            "Gözün kakarırıyor"
            "Ve yatağında uynaıyorsun"
            "Yine aynı odadasın "
            "Doğrulup telefonuna bakıyorsun "
            "saat 02:18 "
            "Ve bir bildirim var"
            "Bugünden değil gelecekten"
            "Ve şöyle diyor en yaptın bilmiyorum||"
            "Ama doğru olanı yaptın"
        ),
        "ending_id": "END_ATTACK_SURRENDER",
    },

    "END_ATTACK_DISARM_ATTEMPT": {
        "text": (
            "Genç halin sana bakıyor.||"
            "Gözleri ‘soru’ değil… ‘öfke’.|||"
            "O zaten kararnı vermiş "
            "Sen bir adım öne çıkıyorsun.|||"
            "Sen: \"Yapma.\"|||"
            "Ama kelime havada kalıyor.|||"
            "Silahına davranıyor ve:|||"
            "Hademe karnını tutmaya başlıyor…||"
            "hademe nefes nefese kalıyor…||"
            "Ve yere yığılıyor …|||"
            "Son nefesiyle 'herşey benim suçumdu'.|||"
            "Genç haline bakıyorsun sen ne yaptın der gibi"
            "Bana öyle bakamyı kes bunu yapmak zorundaydım"
            "Hademe o zamanı bir arada tutmadığı için ozaman yokolmaya başlıyor"
            "Saatler 02:18i göstermeye başlıyor"
            "Portaldan geçmekten başka bi seçeeğiniz yok"
            "Genç haline bakıp diyorsunki "
            "Bakalım gelcek bize ne getirecek"
            "Sana bakıp gülümsüyor ve diyorki"
            "Daaha kötü olamaz"
        ),
        "ending_id": "END_ATTACK_DISARM_ATTEMPT",
    },

    "S15_RAY_VENT_ESCAPE_SOLO": {
        "text": (
            "Gözlerin karanlığa alışırken tavandaki metal ızgarayı fark ediyorsun.||"
            "Havalandırma.|||"
            "Ama çok yüksekte"
            "birinin diğerini kaldırması gerek"
            "ORTANCA: \"Madem yanlız birimiz burdan çıkabilir bu sen olmalısın \"|||"
            " \"İtiraz etmiyorsun  \"|||"
            "Ellerin ızgaraya gidiyor.||"
            "Vida yok.||"
            "Sadece eski, gevşek bir kilit.|||"
            "Parmaklarını araya sokuyorsun.||"
            "Çıt.|||"
            "Izgara hafifçe açılıyor.||"
            "İçeriden kuru, tozlu bir hava yüzüne vuruyor.|||"
            "Sürünerek içeri giriyorsun.||"
            "Omuzların zor sığıyor.|||"
            "Karanlık bir tünel.||"
            "Her hareketinde metal inliyor.|||"
            "Bir yerde tünel ikiye ayrılıyor gibi.||"
            "Hangisi doğru bilmiyorsun.|||"
            "Ama bir şeyi biliyorsun:||"
            "Geri dönmeyeceksin.|||"
            "Bir çıkış ızgarası.|||"
            "İtiyorsun.||"
            "Kendini dışarı bırakıyorsun.|||"
            "Kafeterya koridoru.||"
            "Boş gibi…|||"
            "Ama ışıklar titriyor.||"
            "Sanki senin geldiğini haber veriyor."
        ),
        "auto_next": "END_SOLO_ESCAPE",
    },

    "S16_CHESS_PUZZLE_SCREEN": {
        "images": [None, "images/s16_chess_puzzle_screen.png", None],
        "text": (
            "##Tahtaya bakıyorsun.||"
            "Taşlar sana bir şey ima ediyor.|||"
            "Oyun sonu çok yakın gibi.||"
            "Taşların koordinatları sana bir şeyler anlatıyor.|||"
            "Şifre bu olabilir mi?||"
            "Ama hangi taş ve hangi koordinat?|||"
            "Biraz düşündükten sonra fark ediyorsun:||"
            "BULDUM! Tek hamlede mat var.|||"
            "ŞİFRE BU OLMALI."
        ),
        "choices": {
            "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A", []),
            "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
            "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
        },
    },

    "S16_CHESS_TRY_A": {
        "images": [None, "images/s16_chess_try_a.png", None],
        "text": (
            "##Kale h7 gibi ama emin değilim .||"
            "Ozaman şifre h7 olabilirmi.||"
            "Denemekten zarar gelmez herhalde:||"
        ),
        "choices": {
            "1": ("Şifreyi deneyelim bakalım", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_CHESS_TRY_B": {
        "images": [None, "images/s16_chess_try_b.png", None],
        "text": (
            "##Atı g6'ya oynuyorsun.||"
            "Ozaman şifre g6 olabilirmi.||"
            "Denemekten zarar gelmez herhalde:||"
        ),
        "choices": {
            "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_CHESS_TRY_C": {
        "images": [None, "images/s16_chess_try_c.png", None],
        "text": (
            "##Atı f7'ya oynuyorsun.||"
            "Ozaman şifre f7 olabilirmi.||"
            "Denemekten zarar gelmez herhalde:||"
        ),
        "choices": {
            "1": ("Kilide yönel", "S16_UNLOCK_SEQUENCE", []),
            "2": ("Boşverip yangın \n tüpüyle kilidi kır", "S16_yangın_tüpü", []),
            "3": ("Yakalanmadan saklan ", "S16_CAFETERIA_HIDE", []),
        },
    },

    "S16_UNLOCK_SEQUENCE": {
        "images": [None, "images/s16_1_counter_back copy.png", None],
        "text": (
            "##Tezgâhın altına eğiliyorsun.||"
            "Şifreli olan kilidi şifreni girmeye hazırlanıyorsun.||"
        ),

        "choices": {
            "1": ("h7 ", "S16_kilit_açılmıyor_a", []),
            "2": ("g6", "S16_şifre_doğru", []),
            "3": ("f7", "S16_kilit_açılmıyor_C", []),
        },
    },

    "S16_kilit_açılmıyor_a": {
        "text": (
            "##Yanlış hesaplamış olmalıyım.||"
            "Bidaha denemeliyim .||"
        ),"images": [None, "images/s16_kilit_acilmiyor_a.png", None],

        "choices": {
            "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_Again", []),
            "2": ("Yangın söndürücüyü al", "S16_şifre_doğru", []),
            "3": ("SAKLAN !!!", []),
        },
    },
        "S16_kilit_açılmıyor_c": {
        "text": (
            "##Yanlış hesaplamış olmalıyım.||"
            "Bidaha denemeliyim .||"
        ),"images": [None, "images/s16_kilit_acilmiyor_c.png", None],

        "choices": {
            "1": ("Tekrar tahtaya bak", "S16_CHESS_PUZZLE_SCREEN_Again", []),
            "2": ("Yangın söndürücüyü al", "S16_şifre_doğru", []),
            "3": ("SAKLAN !!!", []),
        },
    },
    "S16_CHESS_PUZZLE_SCREEN_Again": {
        "images": [None, "images/s16_chess_puzzle_screen.png", None],

        "text": (
            "##Tekrar tahtaya bakıyorsun.||"
            "Bu sefer doğru hamleyi yapman gerek."
        ),
        "choices": {
            "1": ("Kale h7'ye oynar", "S16_CHESS_TRY_A", []),
            "2": ("At g6'ya oynar", "S16_CHESS_TRY_B", []),
            "3": ("At f7'ye oynar", "S16_CHESS_TRY_C", []),
        },
    },

    "S16_şifre_doğru": {
        "text": (
            "##Biliyordum.||"
            "Kilit açıldı.||"
            "İçinde bir anahtar var.||"
        ),"images": [None, "images/s16_sifre_dogru.png", None],

        "choices": {
            "2": ("Anahtarı al", "S16_KEY_TAKEN_SOLO", ["I_KEY"]),
        },
    },

    "S16_KEY_TAKEN_SOLO": {
        "text": (
            "##Anahtarı aldın.||"
            "Ne açtığını bilmiyorsun ama doğru olduğunu hissediyorsun.|||"
            "Tam cebine koyacakken…|||"
            "Yan taraftaki kapıdan bir ses geliyor.||"
            "Hafif bir tıkırtı.||"
            "Sanki biri kapının arkasında nefes alıyor.|||"
            "Kafeterya koridoru ise bomboş.||"
            "Işıklar titriyor."
        ),"images": [None, "images/s16_key_taken_solo.png", None],

        "choices": {
            "1": ("Yangın çıkışına doğru git", "END_SOLO_ESCAPE_A", []),
            "2": ("Ses gelen deponun kapısına doğru yaklaş", "S15_CAFETERIA_STORAGE_LOCK", []),
        },
    },

    "S16_RAY_TO_S15_CAPTURE": {
        "text": (
            "Kapıya yaklaşıyorsun.||"
            "Ses çok yakın….|||"
            "Elin, istemsizce anahtarı sıkıyor.||"
            "Metal avucunda sıkıca duruyor.|||"
            "Kulağını kapıya yaklaştırıyorsun.||"
            "içeriyi duymak için.||"
            "Ve tam o boşlukta—|||"
            "Arkandan bir gölge düşüyor.||"
            "Ne olduğunu anlamadan bileğin kavranıyor.|||"
            "Hademe.||"
            "Tek kelime etmeden seni çekiyor.|||"
            "Kapı açılıyor.||"
            "İçeriden ağır bir depo kokusu vuruyor.|||"
            "Bir itiş…||"
            "Kapı kapanıyor.||"
            "Kilit sesi."
        ),
        "auto_next": "S15_CAFETERIA_STORAGE_LOCK",
    },
"END_SOLO_ESCAPE_A": {
    "layout": "single_focus",
    "image": "images/scene_corridor.png",
    "flicker": {"index": 2, "slot": "C", "intensity": "strong"},

    "text": (
        "##Kafeteryadan fırlıyorsun.||"
        "Koridorun ucunda, paslı bir tabela:||"
        "YANGIN ÇIKIŞI.|||"
        "Kapının etrafındaki ışık diğerlerinden farklı...□||"
        "Garip bi his veriyo.|||"
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
        "Arkana bakıyorsun—||"
        "Hademe beliriyor.|||"
        "Yaşlı… omuzları çökmüş… ama gözleri keskin.||"
        "Koşamıyor.||"
        "Ama seni durdurmaya çalışıyor.|||"
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
        "Sen kapıya doğru hızlanıyorsun.||"
        "Elin kolu titreyerek anahtarı çıkarıyorsun.□|||"
        "Kilit…□||"
        "Tık.|||"
        "Kapıyı açıyorsun ve—||"
        "Bu bir kapı değil.|||"
    ),

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
         "Kapının içinde… dönüp duran bir boşluk var.||"
        "Işık değil□— sanki zamanın kendisi kıvrılıyor.||"
        "Bir ZAMAN PORTALI.|||"
        "Hademe arkanıdan bağırıyor:□||"
        "\"Dur!\"□||"
        "\"Her şeyi mahvedeceksin!\"|||"
        "Sesi çatlıyor.□||"
        "Parmakların kapı kolunda.||"
        "Bir adım…"
    ),
    "choices": {
        "1": ("Hademeye neler olup bittiğini sor", "END_SOLO_ESCAPE_ASK", []),
        "2": ("Kapıdan geç", "END_SOLO_ESCAPE_PORTAL", []),
    },
},




    "END_SOLO_ESCAPE_PORTAL": {
        "text": (
            "Kapıdan geçiyorsun.|||"
            "Ne ‘özgürlük’ diyebiliyorsun…||"
            "Ne ‘kaçış’.|||"
            "Sadece… geçiyorsun.|||"
            "Hademe arkandan bağırıyor .||"
            "Dur herşeyi mahvediceksin .|||"
            "Ona aldrırış etmeden portaldan geçiyorsun  .|||"
            "—|||"
            "Gözlerini açıyorsun.|||"
            "Yatak.||"
            "Tavan.||"
            "Odanın kokusu.|||"
            "Her şey… aynı.|||"
            "Doğrulup saate bakıyorsun.||"
            "Saat: 02:18.||"
            "Ama neden herşey yolunamı girdi"
            "Tam o sırada bir ses duyuyosun "
        ),
        "ending_id": "END_SOLO_ESCAPE_PORTAL",
    },

    "END_SOLO_ESCAPE_ASK": {
        "text": (
            "Yutkunuyorsun.||"
            "\"Bunu neden yapıyorsun?\"|||"
            "\"Bu kapı ne?\"|||"
            "\"Neden bu zamanda sıkışıp kaldım?\"|||"
            "Hademe birkaç adım daha atıyor.||"
            "Nefes nefese… ama gözlerini senden ayırmıyor.|||"
            "\"Ben…\"||"
            "Cümle boğazında takılıyor.|||"
            "\"Ben, bunların hepsini ben başlattım.\"|||"
            "Nasıl yani diye soruyorsun.||"
            "Hiç geçmişe gidip bir şeyleri yeniden başlatmak istedin mi?|||"
            "\"Her şeyi düzeltmek…\"||"
            "\"Ben istedim.\"|||"
            "\"Karımı ve kızımı kaybettikten sonra.\"|||"
            "Benim hatamdı. Onları korumalıydım.||"
            "Ama yapamadım.|||"
            "\"Her şeyimi kaybetmiştim.\"|||"
            "\"Ama bir gün ikinci bir şans yaratmanın mümkün olduğunu öğrendim.\"||"
            "\"Karımı ve kızımı kurtarabilirdim.\"||"
            "\"Öyle de yaptım.\"|||"
            "Zaman portalını o kaza gününe ayarladım.||"
            "Nihayet o kazayı hiç yaşanmamış kılabilecektim.|||"
            "\"Öyle de yaptım.\"|||"
            "Bir süre mutluydum.||"
            "Hayatım tekrar karımla ve kızımla mutlu olduğum günlere geri dönmüştü.|||"
            "Sonra ne oldu?|||"
            "Zamanla ilgili bilmen gereken şey şu:|||"
            "Ne kadar kurcalarsan o kadar kontrolden çıkar.|||"
            "Bir süre sonra yaptığım değişikliğin bedelini ödedim.|||"
            "Kendi zamanım içine çöktü.||"
            "Tamamen karanlık ve boş bir zaman…|||"
            "\"Milyarlarca hayat… o zamanda yaşayan insanlar…\"|||"
            "Kiminin geleceği, kiminin geçmişi…||"
            "Hepsi yok oldu. Zamanın içinde bir yarık açıldı.|||"
            "Yaptığım hatayı fark ettiğimde her şey çok geçti.|||"
            "\"Ama yaptığım şeyi düzeltebilirdim.\"|||"
            "30 yıl öncesine gittim.||"
            "Genç halime bunu anlattım ve durması gerektiğini söyledim.|||"
            "\"Ama bunu anlayamayacak kadar kibirli ve toydu.\"|||"
            "Ben de ona engel olamayacak kadar yaşlıydım.|||"
            "O yüzden daha da geçmişe gitmeye karar verdim.|||"
            "Yılanın başını küçükken ezmeye.||"
            "Ama tam oradan ayrılırken genç halim beni takip etti.||"
            "Ve bu zamanda sıkıştık… hepimiz.|||"
            "Ve seni buradan kurtarıp yaptığım şeye engel olmaya çalışıyordu.|||"
            "\"O yüzden onu durdurdum.\"|||"
            "Şimdi de seni durduracaM.||"
            "Zamanı korumak zorundayım."
        ),
        "choices": {
            "1": ("Kal ve zamanı koru", "END_SOLO_STAY_PROTECT_TIME", []),
            "2": ("Ayrıl ve özgür ol", "END_SOLO_LEAVE_FREE", []),
        },
    },

    "END_SOLO_STAY_PROTECT_TIME": {
        "text": (
            "Hademe elini uzatıyor.||"
            "Bu fedakarlığı yapmak zorundayız.||"
            "Portal arkanda dönmeye devam ediyor.||"
            "Ama sesi artık daha kısık.|||"
            "Kapıyı kapatıp kilitliyorsun.|||"
            "Sanırım haklısın.||"
            "Bu fedakarlığı yapmalıyım.|||"
            "İnsanlığı kurtarmak için||"
            "Ve orda kalıyorsun.|||"
            "Yıllar boyunca.\\\"|||"
            "Hayatın boşa geçiyor.\\\"|||"
            "Ama en azından biliyorsun.\\\"|||"
            "Zaman artık güvende.\\\"|||"
        ),
        "ending_id": "END_SOLO_STAY_PROTECT_TIME",
    },

    "END_SOLO_LEAVE_FREE": {
        "text": (
            "Geri çekilmiyorsun.||"
            "Bir adım ileri gidiyorsun.|||"
            "Hademe ‘dur’diye sesleniyor.||"
            "Herşeyi mahvediceksin.|||"
            "Hapis ve güvenli bi ömür geçirmektense.||"
            "Özgür bi bilinmez bi sonu tercih ederim.|||"
            "Portalın içi dalgalanıyor.||"
            "\"Özgürlük,\" diyorsun.||"
            "\"Buna ihtiyacım var.\"|||"
            "Hademenin sesi çok kısık:|||"
            "\"Özgürlük değil o…\"||"
            "\"O bir son.\"|||"
            "Geçiyorsun.|||"
            "Gözlerin yanıyor.||"
            "Kulakların uğulduyor.|||"
            "Dünya… bir anlığına üst üste biniyor.|||"
            "Ve sonra—|||"
            "Sessizlik.|||"
            "Yatağında uyanıyorsun.||"
            "Herşey aynı.|||"
            "Gine aynı oda .|||"
            "Az önce yaşadıklarım bir rüyamıydı.|||"
            "Doğrulup telefoan bakıyorsun:|||"
            "Saat: 02:18|||"
            "Sanki bişeyleri doğru yapmış gibisin:|||"
            "\"Ama kim bilir bunu zaman göstericek .\""
        ),
        "ending_id": "END_SOLO_LEAVE_FREE",
    },




"S09_LOOP_ROOM": {
    "text": (
        "##Yatağındasın.||"
        "Aynı oda.||"
        "Yine 02:17.||"
        "Ama bu sefer fark ediyorsun neden zaman ilerlemiyo."
    ),
"images": [
        None,
        "images/s09_loop_room.png",
        None,
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla dışarı çıkı", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S09_LOOP_ROOM_after_cleaner_men": {
    "text": (
        "##Karnına doğru bi hamle yaptın.||"
        "Ama senin yumruğunu tutup seni yere yatırdı||"
        "Ve seni odana geri postaladı||"
        "Bi hademe neden dövüşmeyi bilirki amk."
    ),
"images": [
        None,#('dövüş sahneleri'),
        "images/s09_loop_room.png",
        None,
    ],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk ve tekrar koridora çık", "S04_CORRIDOR_after_fight", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},
"S09_LOOP_ROOM_1": {
    "text": (
        "##Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Dakikalar geçmiyor.||"
        "Telefonun ekranı bile aynı saniyede takılı kalmış gibi.||"
        "Bu bir bekleme değil… kilit."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Bu daha önce oldu", "S10_MEMORY_GLITCH", []),
        "2": ("Hızla ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E02", []),
    },
},

"S09_LOOP_ROOM_2": {
    "text": (
        "##Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Nefes alıyorsun ama göğsün sanki geç tepki veriyor.||"
        "Ellerini oynatıyorsun… gecikmeli.||"
        "Bedenin burada, sen bir tık geridesin."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Zorla hatırlamaya çalış", "S10_MEMORY_GLITCH", []),
        "2": ("Ayağa kalk", "S04_CORRIDOR", []),
        "3": ("Hiç hareket etme", "END_E02", []),
    },
},

"S09_LOOP_ROOM_3": {
    "text": (
        "##Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Duvarlar tanıdık… ama neden tanıdık olduğunu bilmiyorsun.||"
        "Bir şeyi az önce gördün gibi.||"
        "Hatırlamayı denedikçe aklın kayıyor."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Hatırayı zorla", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Gözlerini kapat", "END_E03", []),
    },
},

"S09_LOOP_ROOM_4": {
    "text": (
        "##Yatağındasın.||"
        "Aynı oda.||"
        "Saat 02:17.||"
        "Oda bu sefer sessiz değil.||"
        "Sessizlik… seni izliyor gibi.||"
        "Bir suç duygusu geliyor, ama kime ait bilmiyorsun."
    ),
    "images": [None, "images/s09_loop_room.png", None],
    "choices": {
        "1": ("Artık kaçma", "S10_MEMORY_GLITCH", []),
        "2": ("Koridora çık", "S04_CORRIDOR", []),
        "3": ("Kıpırdama", "END_E04", []),
    },
},


    "S10_MEMORY_GLITCH": {
        "text": (
            "##Başın dönüyor.||"
            "Bir an her şey üst üste biniyor.||"
            "##Koridor.||"
            "Sesler.||"
            "##Bir tartışma."
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
    "text": "##Kamera odasındasın.||Ekranlar açık.||Koridorda biri var.",
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
        "##Görüntüdeki kişi başını çeviriyor.||"
        "Görüntüdeki kişi gözüküyor ama net değil."
    ),
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
    "##Yakınlaştırıyorsun.||"
    "Pikseller büyüyor, görüntü daha da bozuluyor.||"
    "Ama bir anlığına…||"
    "yüz hatları tanıdık geliyor.||"
    "Çok tanıdık.||"
    "Sanki aynaya bakmak gibi… ama değil."
  ),
  "choices": {
    "1": ("Artık burada işin kalmadı, odadan çık", "S04_CORRIDOR_After_camera", []),
    "2": ("Bir kez daha zoom", "S11.3_CAMERA_AUTO_SHUTDOWN", [])
  },
}
,
"S11.3_CAMERA_AUTO_SHUTDOWN": {
    "layout": "triptych",
    "text": (
        "##Bir kez daha yakınlaştırmaya çalışıyorsun.||"
        "Daha net görebilmek için.||"
        "##Bir anda monitörler tek tek sönmeye başlar.||"
        "##Cidden mi?||"
        "Bunun sırası mıydı…||"
        "Karanlıkta kalmak iyi bir fikir değil.||"
        "Bir an önce buradan çıkmalıyım."
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
    "##Biri olup olmadığını kontrol ediyorsun .||"
    "Yok gibi.||"
    "Sanırsam ||"
    
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
        "##Temizlikçi arabaya yaslanıp seni süzüyor.||"
        "Yine mi sen? diyor.||"
        "Geçen sefer de aynı saatti. 02:17.||"
        "Yüzünde tatminsiz bir ifadeyle.||"
        "Biraz da yorgun gibi.||"
    ),
    "images": [
        None,
        "images/s13_janitor_dialogue.png",
        None,
    ],
    "choices": {
        "1": ("Geçen sefer ne demek?", "S16_JANITOR_INFO", []),
        "2": ("Aniden kafeteryaya koş ", "S8.6_go_to_caffeteria", []),
        "3": ("Yalan söylediğini ima et", "S8.4_ANSWER_HİM2", []),
    },
},

    "S8.4_ANSWER_HİM2": {
        "text": (
            "##YALAN SÖYLÜYORSUN.||"
            "Sana güvenmiyorum.||"
            "Bunu pek hoş karşılamyan bi ses tonu ve bakışla.||"
            "Çabuk odana dön.||"
            "Bu sana son uyarım.||"
        ),
        "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
        "choices": {
            "1": ("Haddini bildir", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
"S14_PRE_CONFRONT": {
    "layout": "single_focus",
    "text": (
        "Nefesin hızlanıyor.||"
        "Zihninde görüntüler parçalanıp birleşiyor.|||"
        'Bir an '
        "Bir tartışma.|||"
        "-Bunu yapmana izin veremem."
    ),
    "image": "images/s14_pre_confront.png",

    # ✅ Memory glitch / blur pulse efekti
    "dizzy": {"mode": "blur", "intensity": "strong", "speed_ms": 60},

    "choices": {
        "1": ("kendini topla ve koridora çık", "S04_CORRIDOR", []),
    },
},


"S16_JANITOR_INFO": {
    "text": (
        "Bir süre susuyor.||"
        "Bazı geceler bazen geçmez , diyor.|||"
        "İnsanlar ya fark etmez...||"
        "ya da fark ettiğinde çok geç olur.|||"
        "Sonra fısıldıyor:||"
        "\"Kamera odasına gittin mi?\""
    ),
    "images": [
        None,
        "images/s16_janitor_info.png",
        None,
    ],
    "choices": {
        "1": ("Evet de (yalan söyle)", "S8.4_ANSWER_HİM3", []),
        "2": ("Hayır de", "S17_JANITOR_REACT", []),
        "3": ("Ayak seslerini sor", "8.4_ANSWER_HİM4", []),
    },
},
     "S8.4_ANSWER_HİM4": {
        "text": (
            "Ayak sesimi.||"
            "Burda tüm gece sadece ben vardımm.|||"
            "Beli benim ayak sesimi duymuşsundur.||"
            "Merak etme .||"
            
        ),
        "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
        "choices": {
            "1": ("Tehtidine karşılık ver", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
    "S8.4_ANSWER_HİM3": {
        "text": (
            "##Pek hoş karşılamyan bi ses tonu ve bakışla.||"
            "Bana yalan söylemen hiç hoşuma gitmedi.|||"
            "Az önce ordaydım.||"
            "Şimdi çabuk odana dön.||"
            "Bu sana son uyarım.||"
        ),
        "images": [None, "images/S08.5_DONT_LOOK_HİM", None],
        "choices": {
            "1": ("Tehtidine karşılık ver", "S09_LOOP_ROOM_after_cleaner_men", ["O3"]),
            "2": ("Kafeteryaya doğru koş", "S8.6_go_to_caffeteria", []),
            "3": ("Onu dinle ve odana geri dön", "S09_LOOP_ROOM_3", []),
        },
    },
"S17_JANITOR_REACT": {
    "text": (
        "Gözlerini kısıyor.||"
        "Aradığın cevapları orada bulacaksın.||"
        "Ama dikkatli ol.||"
    ),
    "images": [
        None,
        "images/s17_janitor_react.png",
        None,
    ],
    "choices": {
        "1": ("Kafeteryaya kaç", "S8.6_go_to_caffeteria", []),
        "2": ("Kamera odasına git", "S07_CAMERA_DOOR", []),
        "3": ("Odaya geri dön", "S09_LOOP_ROOM", []),
    },
},

 
"END_E01": {
    "layout": "single_focus",
    "text": (
        "##Gözlerini kapatırsın.||"
        "Ayak sesleri durur.||"
        "Saat değişmiyor."
    ),
    "image": "images/end_e01.png",
    "ending": True,

    # ✅ final ekranda yazacak cümle (son cümle yerine)
    "final_screen_line": "02:17.",

    # ✅ büyük başlık
    "ending_title": "Birinci Son",

    # ✅ müzik
    "ending_music": "sounds/ending_theme.mp3",
    "ending_music_volume": 0.20,
    "ending_music_start": True,

    # timing
    "final_hold_ms": 3000,
    "final_fade_ms": 1800,

    # title pop
    "title_pop_ms": 180,
    "title_pop_steps": 10,
    "title_font": 56,

    # “Birinci Son” ekranda kalsın, sonra menüye dönsün
    "after_title_ms": 3500,
    "menu_fade_ms": 1600,
    "menu_fade_steps": 24
},


    "END_E02": {"text": "Kıpırdamazsın.||Tik… tak…||||Ayak sesleri yaklaşır.||Bu sefer durmaz.", "image": "images/end_e02.png", "ending": True},
    "END_E03": {
    "layout": "single_focus",
    "image": "images/end_e03.png",
    "text": "Böyle bi ortamda karanlıkta kalmak pek de iyi bir fikir değil.",
    "ending": True,
    "choices": {
        "1": ("Ana Menü", "MAIN_MENU", []),
    },
},
    "END_E04": {"text": "Fişi çekersin.||Ekranlar söner.||Işıklar söner.||||Karanlık.||||Sonra ayak sesleri başlar.||Çıkış yok.", "image": "images/end_e04.png", "ending": True},
    "END_E05": {"text": "Kayıtları silersin.||Bir saniyelik rahatlama.||||Sonra ekranlar şunu yazar:||02:17||||Altında:||\"TEKRAR DENE.\"", "image": "images/end_e05.png", "ending": True},
    "END_E06": {"text": "Gözlerini kapatırsın.||||Açtığında tekrar yatağındasın.||02:17.||Ve nefes daha yakın.", "image": "images/end_e06.png", "ending": True},
    "END_E07": {"text": "Gözlerini kapatırsın.||||Alarm sönümlenir.||Nefes sönümlenmez.||02:17 kalır.", "image": "images/end_e07.png", "ending": True},
    "END_E08": {"text": "Çığlığın binada yankılanır.||||Kimse cevap vermez.||Sadece 02:17’nin sesi kalır.", "image": "images/end_e08.png", "ending": True},
    "END_E09": {"text": "Her şeyi reddedersin.||||Bina bırakır.||Ama sen bırakamazsın.||02:17 seninle kalır.", "image": "images/end_e09.png", "ending": True},
    "END_E10": {"text": "Kapıyı kapatırsın.||||Bir kilit sesi.||Bu sefer içeride kalan sensin.", "image": "images/end_e10.png", "ending": True},
    "END_CAUGHT_WHILE_REALIZING": {
    "text": (
        "Kaçmıyorsun.||"
        "Bakıyorsun.||"
        "Yüz hatları tanıdık… ama nedenini çıkaramıyorsun.|||"
        "Bu an çok kısa sürüyor.||"
        "Arkana dönmeye fırsatın olmuyor.||"
        "Bir kol göğsünü sıkıca kavrıyor.|||"
        "Nefesin kesiliyor.||"
        "Bu gücü tanıyorsun.||"
        "Direnmiyorsun bile.|||"
        "Çünkü geç kaldığını biliyorsun.||"
        "Bir süre sonra yatağındasın.||"
        "Kolların ve bacakların bağlı.|||"
        "Oda karanlık.||"
        "Saat: 02:17.||"
        "Bu sefer kaçmayı denemedin bile."
    ),
    "ending": "CAUGHT_WHILE_REALIZING"
}

}

