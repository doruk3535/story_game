
STORY= {
    "start": {
        "text": "02:17. You wake up in your dorm. Footsteps in the hallway.\nWhat do you do?",
        "choices": {
            "1": ("Hide under the bed", "under_bed"),
            "2": ("Open the door and peek", "peek"),
        }
    },

  
    "under_bed": {
        "text": "You hide. The footsteps stop at your door.\nA shadow passes.\nNow what?",
        "choices": {
            "1": ("Stay completely still", "shadow_passes"),
            "2": ("Turn on phone flashlight", "note_found"),
        }
    },

 
    "peek": {
        "text": "The corridor is empty, but lights flicker.\nYou see a keycard on the floor.",
        "choices": {
            "1": ("Pick up the keycard", "keycard"),
            "2": ("Go back in and lock the door", "lock_in"),
        }
    },

   
    "shadow_passes": {
        "text": "The shadow leaves. You hear an elevator 'ding' far away.\nYou can move.",
        "choices": {
            "1": ("Go to the stairwell", "stairwell"),
            "2": ("Check the corridor first", "corridor"),
        }
    },

   
    "note_found": {
        "text": "You find a note under the desk: 'DON'T TRUST THE ELEVATOR.'",
        "choices": {
            "1": ("Trust the note, take stairs", "stairwell"),
            "2": ("Ignore it, go to elevator", "elevator"),
        }
    },

 
    "keycard": {
        "text": "The keycard says: 'LAB - B2'. There's also a small USB labeled 'logs'.",
        "choices": {
            "1": ("Go to elevator", "elevator"),
            "2": ("Go to stairwell", "stairwell"),
        }
    },

   
    "lock_in": {
        "text": "You lock the door. Someone knocks.\nA calm voice: 'Security. Open up.'",
        "choices": {
            "1": ("Open the door", "bad_end"),
            "2": ("Stay silent", "silent_room"),
        }
    },

  
    "silent_room": {
        "text": "The knocking stops. Minutes pass.\nYou notice the window is slightly open.",
        "choices": {
            "1": ("Climb out the window carefully", "roof"),
            "2": ("Wait until morning", "neutral_end"),
        }
    },

 
    "roof": {
        "text": "You reach the roof. Cold wind.\nYou see stairs down to a maintenance door.",
        "choices": {
            "1": ("Enter the maintenance door", "maintenance"),
            "2": ("Try to climb down the fire ladder", "lobby"),
        }
    },

    "corridor": {
        "text": "You step into the corridor. Lights die.\nA door is open: 'Maintenance'.",
        "choices": {
            "1": ("Enter Maintenance", "maintenance"),
            "2": ("Run to stairwell", "stairwell"),
        }
    },

 
    "maintenance": {
        "text": "Inside maintenance: monitors show your room.\nYou see yourself... sleeping.\nImpossible.",
        "choices": {
            "1": ("Go to stairwell and reach B2", "lab_b2"),
            "2": ("Go to lobby and try to leave", "lobby"),
        }
    },


    "stairwell": {
        "text": "In the stairwell, the air is cold.\nYou can go down or go to lobby.",
        "choices": {
            "1": ("Go down to B2", "lab_b2"),
            "2": ("Go to lobby", "lobby"),
        }
    },

   
    "elevator": {
        "text": "The elevator arrives instantly.\nIt starts moving down without you pressing anything.",
        "choices": {
            "1": ("Jump out before it closes", "stairwell"),
            "2": ("Let it take you to B2", "lab_b2"),
        }
    },


    "lobby": {
        "text": "Lobby is empty. Main door is locked.\nYou see a fire alarm box on the wall.",
        "choices": {
            "1": ("Pull the fire alarm", "good_end"),
            "2": ("Try to force the main door", "bad_end"),
        }
    },

    "lab_b2": {
        "text": "B2 Lab: a terminal lights up: 'USER DETECTED'.\nA button appears: 'EXIT TEST'.",
        "choices": {
            "1": ("Press EXIT TEST", "good_end"),
            "2": ("Smash the terminal", "neutral_end"),
        }
    },

    "good_end": {
        "text": "You escape. Dawn is breaking.\nYour phone buzzes: 'TEST COMPLETE.'",
        "ending": "GOOD ENDING"
    },
    "bad_end": {
        "text": "It was a trap.\nThe last thing you hear is the lock clicking behind you...",
        "ending": "BAD ENDING"
    },
    "neutral_end": {
        "text": "You survive, but nothing really ends.\nTomorrow looks exactly the same.",
        "ending": "NEUTRAL ENDING"
    },
}
STORY_TR = {
    "start": {
        "text": "02:17. Yurtta odanda uyandın. Koridorda ayak sesleri var.\nNe yaparsın?",
        "choices": {
            "1": ("Yatağın altına saklan", "under_bed"),
            "2": ("Kapıyı aralayıp koridora bak", "peek"),
        }
    },

    "under_bed": {
        "text": "Saklanıyorsun. Ayak sesleri kapında duruyor.\nBir gölge geçiyor.\nŞimdi ne yaparsın?",
        "choices": {
            "1": ("Çıt çıkarmadan bekle", "shadow_passes"),
            "2": ("Telefonun fenerini aç", "note_found"),
        }
    },

    "peek": {
        "text": "Koridor boş, ama ışıklar yanıp sönüyor .\nYerde bir anahtar kart görüyorsun.",
        "choices": {
            "1": ("Anahtar kartı al", "keycard"),
            "2": ("Odana git ve kapıyı kilitle", "lock_in"),
        }
    },

    "shadow_passes": {
        "text": "Gölge uzaklaşıyor. Uzaklardan bir asansör 'ding' sesi geliyor.\nArtık hareket edebilirsin.",
        "choices": {
            "1": ("Merdiven boşluğuna git", "stairwell"),
            "2": ("Önce koridoru kontrol et", "corridor"),
        }
    },

    "note_found": {
        "text": "Masasının altında bir not buluyorsun: 'ASANSÖRE GÜVENME.'",
        "choices": {
            "1": ("Nota güven, merdivenleri kullan", "stairwell"),
            "2": ("Görmezden gel, asansöre git", "elevator"),
        }
    },

    "keycard": {
        "text": "Kartın üstünde şu yazıyor: 'LAB - B2'. Ayrıca 'logs' etiketli küçük bir USB var.",
        "choices": {
            "1": ("Asansöre git", "elevator"),
            "2": ("Merdiven boşluğuna git", "stairwell"),
        }
    },

    "lock_in": {
        "text": "Kapıyı kilitliyorsun ama. Biri kapıyı tıklatıyor.\nSakin bir ses: 'Güvenlik. Kapıyı aç.'",
        "choices": {
            "1": ("Kapıyı aç", "bad_end"),
            "2": ("Sessiz kal", "silent_room"),
        }
    },

    "silent_room": {
        "text": "Bi süre sonra tıklatma kesiliyor. Dakikalar geçiyor.\nPencerenin hafif aralık olduğunu fark ediyorsun.",
        "choices": {
            "1": ("Dikkatlice pencereden çık", "roof"),
            "2": ("Sabahı bekle", "neutral_end"),
        }
    },

    "roof": {
        "text": "Çatıya çıkıyorsun. Buz gibi bir soğuk rüzgâr.\nAşağıya inen bir merdiven ve bakım kapısı görüyorsun.",
        "choices": {
            "1": ("Bakım kapısından içeri gir", "maintenance"),
            "2": ("Yangın merdiveninden inmeyi dene", "lobby"),
        }
    },

    "corridor": {
        "text": "Koridora çıkıyorsun. Işıklar sönüyor.\nBir kapı aralık: 'Bakım'.",
        "choices": {
            "1": ("Bakım odasına gir", "maintenance"),
            "2": ("Merdiven boşluğuna koş", "stairwell"),
        }
    },

    "maintenance": {
        "text": "Bakım odasının içinde monitörler var: odanı gösteriyor.\nKendini görüyorsun... uyuyor.\n ama bu İmkânsız.",
        "choices": {
            "1": ("Merdivenlerden B2'ye in", "lab_b2"),
            "2": ("Lobiye git, çıkmayı dene", "lobby"),
        }
    },

    "stairwell": {
        "text": "Merdiven boşluğunda hava buz gibi.\nAşağı inebilir ya da lobiye gidebilirsin.",
        "choices": {
            "1": ("B2'ye in", "lab_b2"),
            "2": ("Lobiye git", "lobby"),
        }
    },

    "elevator": {
        "text": "Asansör anında geliyor.\nHiçbir tuşa basmadan aşağı inmeye başlıyor.",
        "choices": {
            "1": ("Kapanmadan atla", "stairwell"),
            "2": ("B2'ye götürmesine izin ver", "lab_b2"),
        }
    },

    "lobby": {
        "text": "Lobi bomboş. Ana kapı kilitli.\nDuvarda bir yangın alarm kutusu var.",
        "choices": {
            "1": ("Yangın alarmını çek", "good_end"),
            "2": ("Ana kapıyı zorla", "bad_end"),
        }
    },

    "lab_b2": {
        "text": "B2 Laboratuvarı: bir terminal yanıyor: 'KULLANICI TESPİT EDİLDİ'.\nBir buton beliriyor: 'TESTTEN ÇIK'.",
        "choices": {
            "1": ("TESTTEN ÇIK butonuna bas", "good_end"),
            "2": ("Terminali parçala", "neutral_end"),
        }
    },

    "good_end": {
        "text": "Kaçıyorsun. Şafak söküyor.\nTelefonun titriyor: 'TEST TAMAMLANDI.'",
        "ending": "İYİ SON"
    },
    "bad_end": {
        "text": "Bu bir tuzaktı.\nDuyduğun son şey, arkanda kilidin kapanma sesi oluyor...",
        "ending": "KÖTÜ SON"
    },
    "neutral_end": {
        "text": "Hayatta kalıyorsun ama hiçbir şey gerçekten bitmiyor.\nYarın, tıpkı bugün gibi görünüyor.",
        "ending": "NÖTR SON"
    },
}
