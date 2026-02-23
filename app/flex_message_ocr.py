flex_message_ocr = {
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
        "text": "400",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "Payment",
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
            "margin": "xxl",
            "contents": [
              {
                "type": "text",
                "text": "DATE",
                "size": "sm",
                "color": "#555555"
              },
              {
                "type": "text",
                "text": "3",
                "size": "sm",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "TIME",
                "size": "sm",
                "color": "#555555"
              },
              {
                "type": "text",
                "text": "$7.31",
                "size": "sm",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "From",
                "size": "sm",
                "color": "#555555"
              },
              {
                "type": "text",
                "text": "$8.0",
                "size": "sm",
                "color": "#111111",
                "align": "end"
              }
            ]
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "text",
                "text": "To",
                "size": "sm",
                "color": "#555555"
              },
              {
                "type": "text",
                "text": "$0.69",
                "size": "sm",
                "color": "#111111",
                "align": "end"
              }
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
          {
            "type": "text",
            "text": "PAYMENT ID",
            "size": "xs",
            "color": "#aaaaaa",
            "flex": 0
          },
          {
            "type": "text",
            "text": "#743289384279",
            "color": "#aaaaaa",
            "size": "xs",
            "align": "end"
          }
        ]
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}