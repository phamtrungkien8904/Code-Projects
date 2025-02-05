import random
import re
import time

def girlfriend_chatbot():
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
        (r'Kem',): [
            "Dính Ánh! 💞",
            "Nghiện em bé cáaaaa! 💘",
            "Thương em bé Ánh nhứtttt! 😍"
        ],
        (r'Em bé Kem đang làm gì đấy\?',): [
            "Bé Kem đang nhớ bé Ánh! 💭",
            "Bé Kem đang ngắm ảnh Ánh! 💌",
            "Bé Kem đang tương tư Ánh! 🎉"
        ],
        (r'Ai đây\?',): [
            "Áaaaa em bé của Ánh đây màaaaa \n Định mệnh của Ánh đây màaaaa \n Người thương Ánh nhất đây mòooo"
        ],
        (r'T off đây',): [
            "Áaaaaaaaaaa \n Em bé saoooo \n Em bé hem off, ở lại với Kem đê"
        ]
    }

    # Default responses if no pattern matches
    default_responses = [
        "Chụt Ánhhhh 💕",
        "Nghiện Ánhhhh 💕",
        "Dính Ánhhhh 💕",
        "Thương Ánhhhh 💕"
    ]

    print("Kem: Hế nhô bé Ánhhhh! 💖 (Bấm 'quit' để kết thúc đoạn chat).")
    
    while True:
        user_input = input("\nWoy: ").strip()  # Removed .lower()
        
        if user_input.lower() == 'quit':  # Check lowercase for quit
            print("\nKem: Kem thương Ánh nhìuuuu! 💌 Lát dính Ánh nháaa!")
            break
        
        response_found = False
        
        # Check response patterns with case-insensitive flag
        for patterns, responses in response_rules.items():
            if any(re.search(pattern, user_input, re.IGNORECASE) for pattern in patterns):
                print(f"\nKem: {random.choice(responses)}")
                response_found = True
                break
        
        # If no pattern matched, use default response
        if not response_found:
            print(f"\nKem: {random.choice(default_responses)}")
        
        # Add slight delay for more natural feel
        time.sleep(0.5)

# Start the chatbot
girlfriend_chatbot()