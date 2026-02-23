# Flex Message JSON
flex_message = {
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
        "text": "Recieve Money",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
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
              {
                "type": "text",
                "text": "Amount",
                "size": "sm",
                "color": "#555555",
                "flex": 0
              },
              {
                "type": "text",
                "text": "$3.33",
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
            "text": "USER",
            "size": "xs",
            "color": "#aaaaaa",
            "flex": 0
          },
          {
            "type": "text",
            "text": "BO55",
            "color": "#aaaaaa",
            "size": "xs",
            "align": "end"
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "Confirm",
          "uri": "http://linecorp.com/"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "Edit",
          "uri": "https://slip-bot-dashboard.vercel.app/edit-data"
        }
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": True
    }
  }
}