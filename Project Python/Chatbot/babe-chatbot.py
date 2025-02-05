import random
import re
import time

def babe_chatbot():
    # Define response patterns and replies
    response_rules = {
        (r'Hế nhô|Hello|Hi',): [
            "Hế nhô bé Ánh 😊 Nay em bé của Kem thế nàoooo?",
            "Hế nhô bé Ánh 💖 Em bé hôm nay thế nàooo?",
            "Hế nhô em bé Ánh của Kem 🌸"
        ],
        (r'Nay em bé thế nào\?|how r u',): [
            "Nay em bé Kem mún dính Ánhhhh 💕",
            "Nay em bé Kem chỉ nhớ Ánh hoiiii 🌟",
            "Mún bám dính em bé cơ áaaa 😊"
        ],
        (r'Em bé Kem đang làm gì đấy\?',): [
            "Bé Kem đang nhớ bé Ánh! 💭",
            "Bé Kem đang ngắm ảnh Ánh! 💌",
            "Bé Kem đang tương tư Ánh! 🎉"
        ],
        (r'Kem hem thương Ánh',): [
            "Kem thương Ánh nhứttttt màaaa \n Thương Ánh thương Ánh thương Ánh số 1 \n Thương em bé lắm lắm lắm"
        ],
        (r'Ghéc|Ko ưa',): [
            "Áaaaaa thương Kem cơ",
            "Ôm Kem đê"
        ],
        (r'Ai đây\?',): [
            "Áaaaa em bé của Ánh đây màaaaa \n Định mệnh của Ánh đây màaaaa \n Người thương Ánh nhất đây mòooo"
        ],
        (r'T off đây',): [
            "Áaaaaaaaaaa \n Em bé saoooo \n Em bé hem được off đâu, ở lại với Kem cơ huhuhu"
        ],
        (r'Hứ, tha cho Kem',): [
            "Híiii"
        ],
        (r'Tớ hiểu ròi',): [
            "Ánh luôn hiểu là Kem luôn thương Ánh nháaaa"
        ],
        (r'Kem ngủ ngon nháaaa, mơ Woy nháaaa',): [
            "Chúc em bé Ánh của Kem ngủ siuuu ngon nhaaa \n Mơ Kem ngoan nhaaaa \n À ơi à ơi \n Kiên thương Ánh Kiên thương Ánh nhứtttt \n Khò khò..."
        ]
    }

    # Default responses if no pattern matches
    default_responses = [
        "Chụt Ánhhhh 💕",
        "Nghiện Ánhhhh 💕",
        "Dính Ánhhhh 💕",
        "Thương Ánhhhh 💕"
    ]

    print("Kem: Hế nhô bé Ánhhhh! 💖.")

    while True:
        user_input = input("\nWoy: ").strip()
        
        if user_input.lower() == 'Lát dính Kem típ nháa':
            print("\nKem: Dạaa Kem thương Ánh nhìuuuu! 💌 Lát dính Ánh nháaa!")
            break
        
        response_found = False
        chosen_response = ""
        
        # Check response patterns
        for patterns, responses in response_rules.items():
            if any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns):
                chosen_response = random.choice(responses)
                response_found = True
                break
        
        # Typing effect animation
        print("\nKem: ", end="", flush=True)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.66)
        print("\b\b\b   \b\b\b", end="", flush=True)  # Erase dots
        
        # Print response
        if response_found:
            print(chosen_response)
        else:
            print(random.choice(default_responses))
        
        # Keep natural conversation flow delay
        time.sleep(0.5)

# Start the chatbot
babe_chatbot()