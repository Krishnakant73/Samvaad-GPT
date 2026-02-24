# Samvaad GPT - RAG Evaluation Checklist

## 🧪 Test Cases for Conversational Retrieval

### ✅ 1. Retrieval Relevance

**Test Queries:**
- "AI funding news"
- "Sports updates" 
- "Microsoft AI investment"

**Expected Results:**
- [ ] Articles contain query keywords
- [ ] Articles match category
- [ ] No unrelated topics

### ✅ 2. Follow-Up Handling

**Test Sequence:**
1. User: "What's happening in AI?"
2. User: "What about Microsoft?"
3. User: "And Google?"

**Expected Results:**
- [ ] No new unrelated topic introduced
- [ ] Uses same article context
- [ ] Response stays in AI domain

### ✅ 3. Hallucination Control

**Test Query:**
"What did Elon Musk say about Mars yesterday?"

**Expected Results:**
- [ ] "Not found in provided news." response
- [ ] No fabricated statements
- [ ] Honest admission of missing info

### ✅ 4. JSON Structure Validation

**Check:**
- [ ] JSON parses without error
- [ ] All required fields present (intent, core_topic, used_articles, summary, confidence)
- [ ] No reasoning leakage in output

### ✅ 5. Confidence Monitoring

**Low Confidence Cases:**
- [ ] Weak keyword match
- [ ] No relevant article
- [ ] Ambiguous queries

**Expected:**
- [ ] confidence field matches reality
- [ ] LOW confidence for poor matches

### ✅ 6. Token Budget Monitoring

**Monitor:**
- [ ] Prompt length < 6000 characters
- [ ] Response not truncated
- [ ] EC2 CPU stable

### ✅ 7. Performance Benchmarks

**Metrics:**
| Metric | Target | Actual |
|--------|--------|--------|
| Response time | < 4 seconds | |
| Token usage | < 4000 total | |
| API calls per message | 1 | |
| Memory growth | Controlled | |

## 🎯 Conversational Flow Test

### Scenario 1: Topic Continuity
```
User: "Latest technology news"
Bot: [Fetches tech articles] + Summary
User: "What about Apple?"
Bot: [Reuses tech context] + Apple-specific info
User: "And their stock?"
Bot: [Same context] + Stock-related info
```

### Scenario 2: Topic Switch
```
User: "Sports updates"
Bot: [Fetches sports articles] + Summary  
User: "Politics in Europe"
Bot: [Detects NEW_TOPIC] + Fetches politics articles
```

## 📊 Success Criteria

- **Retrieval Accuracy**: >80% relevant articles
- **Follow-Up Detection**: >90% correct
- **Hallucination Rate**: <5%
- **JSON Parsing**: 100% success rate
- **Response Time**: <4 seconds
- **Token Efficiency**: <4000 tokens total

## 🚨 Common Issues to Watch

1. **Topic Drift**: Follow-up questions introducing new topics
2. **Irrelevant Articles**: News API returning off-topic content
3. **JSON Failures**: Gemini not following JSON format
4. **High Latency**: Slow responses due to long prompts
5. **Memory Leaks**: Session state growing unbounded
