# Dot Canvas Examples

## Simple Card

```json
{
  "data": {
    "title": "Canvas API",
    "message": "Hello Dot."
  },
  "windowData": {
    "default": [
      {
        "type": "div",
        "props": {
          "tw": "flex flex-col flex-1 bg-white text-black gap-[8px]",
          "children": [
            {
              "type": "div",
              "props": {
                "tw": "text-28-chillduansans font-bold",
                "children": "{{get inputData \"title\" default=\"\"}}"
              }
            },
            {
              "type": "div",
              "props": {
                "tw": "text-18-chillduansans",
                "style": {
                  "lineClamp": 3,
                  "overflow": "hidden",
                  "textOverflow": "ellipsis"
                },
                "children": "{{get inputData \"message\" default=\"\"}}"
              }
            }
          ]
        }
      }
    ]
  },
  "layoutFull": {
    "tw": "p-0 bg-white",
    "style": {
      "padding": 0
    }
  },
  "border": 0
}
```

## Task List

```json
{
  "data": {
    "tasks": [
      { "title": "Review dashboard", "status": "open" },
      { "title": "Ship release notes", "status": "done" }
    ]
  },
  "windowData": {
    "default": [
      {
        "type": "div",
        "props": {
          "tw": "flex flex-col w-full h-full bg-white text-black gap-[6px]",
          "children": [
            {
              "type": "div",
              "props": {
                "tw": "text-22-chillduansans font-bold",
                "children": "{{formatDate inputData.date \"yyyy/MM/dd\" \"Asia/Shanghai\"}}"
              }
            },
            {
              "type": "div",
              "props": {
                "$for": {
                  "items": "inputData.tasks",
                  "as": "task",
                  "index": "index"
                },
                "$empty": {
                  "type": "div",
                  "props": {
                    "tw": "text-18-chillduansans",
                    "children": "No tasks"
                  }
                },
                "tw": "flex flex-row items-center gap-[6px] min-w-0",
                "children": [
                  {
                    "type": "div",
                    "props": {
                      "tw": "w-[12px] h-[12px] rounded-full border border-black shrink-0",
                      "style": {
                        "backgroundColor": "{{#compare (get task \"status\" default=\"\") \"===\" \"done\"}}#000000{{else}}#FFFFFF{{/compare}}"
                      },
                      "children": ""
                    }
                  },
                  {
                    "type": "div",
                    "props": {
                      "tw": "flex-1 min-w-0 text-18-chillduansans",
                      "style": {
                        "lineClamp": 1,
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                        "whiteSpace": "nowrap"
                      },
                      "children": "{{get task \"title\" default=\"\"}}"
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    ]
  }
}
```
