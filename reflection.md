# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**
- Three Core actions:
    - Add A pet and owner
    - Set preference for tasks
    - generate a daily schedule based on time contraints, priority, and owner preference
- Briefly describe your initial UML design.
    - My uml intends to show that there will be three sub methods, pet, owner, and task that will all be used in the main method to generate a schedule for the owner to follow.
- What classes did you include, and what responsibilities did you assign to each?
    + addPet()
    + createTask()
    + createSchedule()
    + owner()
    - ownerName
    - petName
    - petBreed
    - petOwner
    - taskName
    - timeToComplete
    - perference
    - priority

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    - yes, when asking the AI to suggest changes it mentioned that my current skeleton did not have any time contraint variable and also no real link from task to pet in case an owner has multiple pets. Thus i aksed it to implement these changes to my skeleton.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
