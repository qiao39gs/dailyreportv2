REPORT_JSON_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "daily_report",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "hotTopics": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "category": {"type": "string"},
                            "summary": {"type": "string"},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                            "mentions": {"type": "integer"}
                        },
                        "required": ["name", "category", "summary", "keywords", "mentions"],
                        "additionalProperties": False
                    }
                },
                "sharedResources": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "title": {"type": "string"},
                            "sharedBy": {"type": "string"},
                            "time": {"type": "string"},
                            "summary": {"type": "string"},
                            "keyPoints": {"type": "array", "items": {"type": "string"}},
                            "link": {"type": "string"},
                            "domain": {"type": "string"},
                            "category": {"type": "string"}
                        },
                        "required": ["type", "title", "sharedBy", "time", "summary", "keyPoints", "link", "domain", "category"],
                        "additionalProperties": False
                    }
                },
                "importantMessages": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "time": {"type": "string"},
                            "sender": {"type": "string"},
                            "type": {"type": "string"},
                            "priority": {"type": "string"},
                            "content": {"type": "string"},
                            "fullContent": {"type": "string"}
                        },
                        "required": ["time", "sender", "type", "priority", "content", "fullContent"],
                        "additionalProperties": False
                    }
                },
                "interestingDialogues": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "content": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "speaker": {"type": "string"},
                                        "time": {"type": "string"},
                                        "message": {"type": "string"}
                                    },
                                    "required": ["speaker", "time", "message"],
                                    "additionalProperties": False
                                }
                            },
                            "highlight": {"type": "string"},
                            "topic": {"type": "string"}
                        },
                        "required": ["type", "content", "highlight", "topic"],
                        "additionalProperties": False
                    }
                },
                "questionsAnswers": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "object",
                                "properties": {
                                    "asker": {"type": "string"},
                                    "time": {"type": "string"},
                                    "content": {"type": "string"},
                                    "tags": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["asker", "time", "content", "tags"],
                                "additionalProperties": False
                            },
                            "answers": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "responder": {"type": "string"},
                                        "time": {"type": "string"},
                                        "content": {"type": "string"},
                                        "isBest": {"type": "boolean"}
                                    },
                                    "required": ["responder", "time", "content", "isBest"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["question", "answers"],
                        "additionalProperties": False
                    }
                },
                "analytics": {
                    "type": "object",
                    "properties": {
                        "topicHeatmap": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "topic": {"type": "string"},
                                    "percentage": {
                                        "type": "number",
                                        "minimum": 0,
                                        "maximum": 100,
                                        "description": "百分数数值，范围为0到100。例如30%填写30，不得填写0.3。"
                                    },
                                    "count": {"type": "integer"},
                                    "color": {"type": "string"}
                                },
                                "required": ["topic", "percentage", "count", "color"],
                                "additionalProperties": False
                            }
                        },
                        "chatterboard": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "rank": {"type": "integer"},
                                    "name": {"type": "string"},
                                    "count": {"type": "integer"},
                                    "characteristics": {"type": "array", "items": {"type": "string"}},
                                    "commonWords": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["rank", "name", "count", "characteristics", "commonWords"],
                                "additionalProperties": False
                            }
                        },
                        "nightOwl": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "title": {"type": "string"},
                                "lastTime": {"type": "string"},
                                "messages": {"type": "integer"},
                                "lastMessage": {"type": "string"}
                            },
                            "required": ["name", "title", "lastTime", "messages", "lastMessage"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["topicHeatmap", "chatterboard", "nightOwl"],
                    "additionalProperties": False
                },
                "wordCloud": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "word": {"type": "string"},
                            "size": {"type": "number"},
                            "color": {"type": "string"},
                            "left": {"type": "number"},
                            "top": {"type": "number"},
                            "rotate": {"type": "integer"}
                        },
                        "required": ["word", "size", "color", "left", "top", "rotate"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["hotTopics", "sharedResources", "importantMessages", "interestingDialogues", "questionsAnswers", "analytics", "wordCloud"],
            "additionalProperties": False
        }
    }
}
