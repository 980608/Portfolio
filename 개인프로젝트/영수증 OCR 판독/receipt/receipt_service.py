from db.db_data_save import get_conn
from ocr.ocr_processing import run_ocr
from llm.LLM_processing import analyze_receipt


def process_receipt(task_id, img):

    conn = get_conn()
    cur = conn.cursor()

    try:
        # 1. OCR
        ocr_result = run_ocr(img)

        # 2. LLM
        receipt_data = analyze_receipt(
            ocr_result["ocr_text"]
        )

        # 3. receipt 업데이트
        cur.execute("""
            UPDATE receipt
            SET store_name = %s,
                purchase_at = %s,
                total_price = %s,
                category = %s,
                status = %s
            WHERE task_id = %s
        """, (
            receipt_data.get("storeName", "0"),
            receipt_data.get("purchaseAt", "0"),
            receipt_data.get("totalPrice", 0),
            receipt_data.get("category", "0"),
            "completed",
            task_id
        ))

        # 4. receipt id 조회
        cur.execute("""
            SELECT id FROM receipt WHERE task_id = %s
        """, (task_id,))

        row = cur.fetchone()

        if row:
            receipt_id = row[0]

            # 5. items insert
            for item in receipt_data.get("items", []):

                cur.execute("""
                    INSERT INTO receipt_item
                    (receipt_id, item_name, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """, (
                    receipt_id,
                    item.get("name", "0"),
                    item.get("quantity", 0),
                    item.get("price", 0)
                ))

        conn.commit()

    except Exception as e:

        cur.execute("""
            UPDATE receipt
            SET status = %s
            WHERE task_id = %s
        """, ("failed", task_id))

        conn.commit()

        print("ERROR:", e)

    finally:
        cur.close()
        conn.close()