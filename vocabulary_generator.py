import csv
import os
import re
from collections import Counter
from datetime import datetime
import jieba

def remove_duplicate_verses(text):
    lines = text.strip().split('\n')
    seen = set()
    unique_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped not in seen:
            seen.add(stripped)
            unique_lines.append(line)
    return '\n'.join(unique_lines)

def analyze_multiple_texts():
    print("=== 📚 나만의 빈출 단어장 생성기 ===")

    is_lyrics = input("\n📂 중복되는 구절을 제거할까요? (예: 1, 아니오: 2): ").strip()
    if is_lyrics == '1':
        print("🎵 중복 구절을 제거하고 분석합니다.")
    else:
        print("📝 일반 텍스트 모드로 분석합니다.")

    print("\n💡 [입력 가이드] 여러 개의 파일은 쉼표(,)로 구분하며, 반드시 확장자(.txt)를 포함해야 합니다.")
    file_input = input("▶️ 다중 파일명 입력 (형식: a.txt, b.txt) : ").strip()

    if not file_input:
        print("❌ 입력된 파일명이 없습니다. 프로그램을 종료합니다.")
        return

    file_paths = [f.strip() for f in file_input.split(',')]

    total_word_counts = Counter()
    valid_file_count = 0

    print("\n⏳ 파일 분석을 시작합니다...")

    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"⚠️ '{file_path}' 파일을 찾을 수 없어 분석에서 제외합니다.")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

            if is_lyrics == '1':
                text = remove_duplicate_verses(text)

            cleaned_text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
            words = jieba.lcut(cleaned_text)

            stopwords = ['的', '了', '是', '我', '你', '他', '在', 'the', 'and', 'to', 'of', 'in', 'is', 'it']
            filtered_words = [
                word.strip() for word in words
                if len(word.strip()) >= 1
                and word.strip() not in stopwords
                and not word.strip().isdigit()
            ]

            total_word_counts.update(filtered_words)
            valid_file_count += 1
            print(f"✅ '{file_path}' 분석 완료!")

        except Exception as e:
            print(f"❌ '{file_path}' 처리 중 오류 발생: {e}")

    if valid_file_count == 0:
        print("\n❌ 분석할 수 있는 유효한 파일이 없습니다. 프로그램을 종료합니다.")
        return

    try:
        top_n = int(input("\n단어장에 넣을 상위 단어 개수를 입력하세요 (예: 20): ").strip())
    except ValueError:
        print("⚠️ 숫자를 입력하지 않아 기본값인 20개로 설정합니다.")
        top_n = 20

    common_words = total_word_counts.most_common(top_n)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"my_final_vocabulary_{timestamp}.csv"

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["단어", "총 등장 횟수", "파일당 평균 등장 횟수"])

        for word, total_count in common_words:
            average_count = round(total_count / valid_file_count, 2)
            writer.writerow([word, total_count, average_count])

    print(f"\n🎉 모든 과정 완료! 총 {valid_file_count}개의 텍스트를 분석했습니다.")
    print(f"현재 폴더에 '{output_file}' 파일이 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    analyze_multiple_texts()