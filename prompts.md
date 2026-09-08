

prompt types

# 1 zero-shot prompt: no example. 

    classify sentiment of review
    text: Just had the most incredible authentic feast at IGURU in Manikonda, and I am still dreaming about this meal! 🤤 We started off with the spicy and flavorful Karivepaku Kodi Vepudu, alongside some perfectly crunchy Crispy Corn and Paneer Kurkure.

    Sentiment: Positive ✅

    The review uses strongly positive language such as “most incredible,” “authentic feast,” “still dreaming about this meal,” “spicy and flavorful,” and “perfectly crunchy.”


    classify sentiment of review
    text: I visited this restaurant twice when they started. It used to be so good. Recently, after one year. I again ordered Sahi muttun biryani, some bhimavaram Kodi vepudu. And the waiter suggested to have muttun soup., which is a disaster in taste they served with a big boll joint of sheep which looks quit scary and very uncooked taste

    Sentiment: Negative ❌

    The review is negative because it describes the mutton soup as a “disaster in taste,” mentions a scary-looking, very uncooked sheep bone/joint, and criticizes the overall food quality compared with the restaurant's earlier experience.

# few shot promot: examples

    classify sentiment of review, no emojis and i need response exactly like my examples

    Example 1:
    text: good product at affordable price
    Answer: Positive

    Example 2:
    text: Curry not cooked properly
    Answer: Negative

    text: Food is authentic and tasty. Best in Hyderabad as of today

    Answer: Positive ✅

    text: Worst part: Mutton bones where crushed and mixed in curry so every bite you will get many small bones.
    Their package don't have anything for the people who don't drink, not even basic mocktail. And you have to ask for the Lemonade as well.
    Service: Staff or manager should adapt to repeated requests, they provided watermelon juice and it tasted blant and normal on temperature. We had to ask for the ice every time.
    Same with the basic elements like sugar with curd

    Answer: Negative ❌



# prompt structure


# Role

    1. sales agent
    2. reactjs developer
    3. technical interviewer
    4. business analyst
    5. USA CEO

# task/instructions

    based on candidate goals, profile and background , suggest best suitable course

    based on technologies, experince, company type, -> conduct mock interview







