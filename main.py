import logging
import sys

# Configure logging
logging.basicConfig(
    filename='tournament_app.log',
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Initial match data
matches = [
    {
        "match_id": "M01",
        "team_a": "T1",
        "team_b": "GenG",
        "score_a": 2,
        "score_b": 1,
        "status": "Completed"
    },
    {
        "match_id": "M02",
        "team_a": "JDG",
        "team_b": "BLG",
        "score_a": 0,
        "score_b": 0,
        "status": "Pending"
    }
]


def display_matches(match_list):
    """Hiển thị danh sách trận đấu với định dạng bảng."""
    logging.info("User viewed the match list.")
    print("\n--- LỊCH THI ĐẤU & KẾT QUẢ ---")
    if not match_list:
        print("Hiện chưa có trận đấu nào trong hệ thống.")
        return
    
    print(f"{'Mã trận':<10} | {'Đội A':<15} | {'Đội B':<15} | {'Tỷ số':<8} | {'Trạng thái':<10}")
    print("-" * 80)
    for match in match_list:
        score = f"{match['score_a']}-{match['score_b']}"
        print(f"{match['match_id']:<10} | {match['team_a']:<15} | {match['team_b']:<15} | {score:<8} | {match['status']:<10}")


def add_match(match_list):
    """Thêm trận đấu mới vào danh sách."""
    print("\n--- THÊM TRẬN ĐẤU MỚI ---")
    try:
        match_id = input("Nhập mã trận đấu: ").strip()
        if not match_id:
            print("Mã trận đấu không được để trống.")
            logging.warning("User tried to add a match with empty match ID.")
            return
        
        if any(m['match_id'] == match_id for m in match_list):
            print(f"Lỗi: Mã trận đấu {match_id} đã tồn tại.")
            logging.warning(f"Match ID {match_id} already exists.")
            return
        
        team_a = input("Nhập tên Đội A: ").strip()
        if not team_a:
            print("Tên đội không được để trống.")
            logging.warning("User tried to add a match with empty team name.")
            return
        
        team_b = input("Nhập tên Đội B: ").strip()
        if not team_b:
            print("Tên đội không được để trống.")
            logging.warning("User tried to add a match with empty team name.")
            return
        
        new_match = {
            "match_id": match_id,
            "team_a": team_a,
            "team_b": team_b,
            "score_a": 0,
            "score_b": 0,
            "status": "Pending"
        }
        match_list.append(new_match)
        print(f"Thành công: Đã thêm trận đấu {match_id}.")
        logging.info(f"Match {match_id} added successfully")
        
    except Exception as e:
        logging.error(f"Error adding match: {e}")


def get_valid_score(prompt):
    """Helper: Nhập điểm số hợp lệ (số nguyên >= 0), lặp lại nếu sai."""
    while True:
        try:
            score_input = input(prompt).strip()
            score = int(score_input)
            if score < 0:
                print("Điểm số phải lớn hơn hoặc bằng 0.")
                logging.error(f"Negative score input detected: {score_input}")
                continue
            return score
        except ValueError:
            print("Điểm số phải là số nguyên. Vui lòng nhập lại.")
            logging.error(f"Invalid score input. Error: invalid literal for int() with base 10: '{score_input}'")


def update_score(match_list):
    """Cập nhật tỷ số trận đấu."""
    print("\n--- CẬP NHẬT TỶ SỐ TRẬN ĐẤU ---")
    try:
        match_id = input("Nhập mã trận đấu cần cập nhật: ").strip()
        match = next((m for m in match_list if m['match_id'] == match_id), None)
        
        if not match:
            print(f"Không tìm thấy trận đấu mang mã {match_id}.")
            logging.warning(f"User tried to update non-existing match {match_id}")
            return
        
        print(f"Trận đấu: {match['team_a']} vs {match['team_b']} ({match['status']})")
        
        score_a = get_valid_score("Nhập điểm Đội A: ")
        score_b = get_valid_score("Nhập điểm Đội B: ")
        
        # Xử lý đặc biệt tỷ số 0-0
        if score_a == 0 and score_b == 0:
            confirm = input("Tỷ số đang là 0-0. Trọng tài có xác nhận trận đã hoàn thành không? (y/n): ").strip().lower()
            if confirm != 'y':
                match['score_a'] = score_a
                match['score_b'] = score_b
                print("Thành công: Đã cập nhật tỷ số trận đấu (giữ Pending).")
                logging.info(f"Match {match_id} score updated (0-0, not confirmed completed)")
                return
        
        match['score_a'] = score_a
        match['score_b'] = score_b
        match['status'] = "Completed"
        print(f"Thành công: Đã cập nhật tỷ số trận đấu {match_id}.")
        logging.info(f"Match {match_id} score updated successfully")
        
    except Exception as e:
        logging.error(f"Error updating score: {e}")


def determine_winner(match):
    """Xác định đội thắng trận đấu.
    
    Args:
        match (dict): Thông tin trận đấu.
    
    Returns:
        str: Tên đội thắng, "Draw", hoặc "Not Started".
    """
    try:
        if match.get('status') == "Pending":
            return "Not Started"
        if match['score_a'] > match['score_b']:
            return match['team_a']
        elif match['score_b'] > match['score_a']:
            return match['team_b']
        else:
            return "Draw"
    except (KeyError, TypeError):
        return "Unknown"


def generate_report(match_list):
    """Tạo báo cáo thống kê."""
    logging.info("User generated tournament report.")
    print("\n--- BÁO CÁO THỐNG KÊ GIẢI ĐẤU ---")
    
    completed = 0
    for match in match_list:
        if match.get('status') == "Completed":
            winner = determine_winner(match)
            print(f"{match['match_id']}: {match['team_a']} {match['score_a']}-{match['score_b']} {match['team_b']} | Kết quả: {winner}")
            completed += 1
    
    if completed == 0:
        print("Chưa có trận đấu nào hoàn thành.")
    print(f"Tổng số trận đã hoàn thành: {completed}")


def show_menu():
    """Hiển thị menu."""
    print("\n===== HỆ THỐNG QUẢN LÝ GIẢI ĐẤU RIKKEI ESPORTS =====")
    print("1. Hiển thị lịch thi đấu & Kết quả")
    print("2. Thêm trận đấu mới")
    print("3. Cập nhật tỷ số trận đấu")
    print("4. Báo cáo thống kê")
    print("5. Thoát chương trình")
    print("=" * 50)


def main():
    """Chạy chương trình chính."""
    while True:
        show_menu()
        try:
            choice = input("Chọn chức năng (1-5): ").strip()
            if choice == "1":
                display_matches(matches)
            elif choice == "2":
                add_match(matches)
            elif choice == "3":
                update_score(matches)
            elif choice == "4":
                generate_report(matches)
            elif choice == "5":
                logging.info("System shutdown.")
                print("Cảm ơn bạn đã sử dụng hệ thống!")
                break
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1-5.")
                logging.warning("Invalid menu choice selected.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()