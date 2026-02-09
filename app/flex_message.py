from linebot.v3.messaging import FlexMessage

def receipt_flex(result, profile_name):
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "RECEIPT",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "Payment",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": result["refid"],
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "Date", "size": "sm", "color": "#555555"},
                                {"type": "text", "text": result["date"], "size": "sm", "align": "end"}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "Time", "size": "sm", "color": "#555555"},
                                {"type": "text", "text": result["time"], "size": "sm", "align": "end"}
                            ]
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "From", "size": "sm", "color": "#555555"},
                                {"type": "text", "text": result["sender"] or "-", "size": "sm", "align": "end"}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "To", "size": "sm", "color": "#555555"},
                                {"type": "text", "text": result["receiver"], "size": "sm", "align": "end"}
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "Amount", "size": "sm", "color": "#555555"},
                                {"type": "text", "text": f'{result["amount"]} ฿', "size": "sm", "align": "end"}
                            ]
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {"type": "text", "text": "Send By", "size": "xs", "color": "#aaaaaa"},
                        {"type": "text", "text": profile_name, "size": "xs", "align": "end", "color": "#aaaaaa"}
                    ]
                }
            ]
        }
    }

    return FlexMessage(
        alt_text="Payment Receipt",
        contents=bubble
    )
