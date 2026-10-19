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
    my scheduler considers the users choice to perform tasks at varying time throughout the day and instead opts to provide a list without times and instead just in a preferred order based on priority and time taken to complete.
- How did you decide which constraints mattered most?
    - I used personal preference to be honest and the idea that people's schedules are often changing and fluid so it made more sense to have a scheduler be more of a "task organizer" than with actual times.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - My program checks for exact name and pet matches instead of focusing on time matches in order to prevent duplicate tasks unless needed.
- Why is that tradeoff reasonable for this scenario?
    - this tradeoff is reasonable because the program assumes the user can deduct that tasks around the same time will be done one after the other.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used AI to design, debug, and even build parts of the code, it was very helpfull in identifying problems and constantly updating the test cases to match the new code. 
- What kinds of prompts or questions were most helpful?
    - prompts that clearly outlined details of what i wanted implemented with context where the most helpfull. If i vaguely asked for the AI to create and algorithm to streamline my code it would start making changes everywhere instead of exactly where I wanted it to.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - The AI at one point wanted to impliment a repeating task functionality where you could input an amount of time between tasks, but for the sake of this scheduler I believed it made more sense to have the tasks be either daily or not.
- How did you evaluate or verify what the AI suggested?
    - I checked where the compiler identified changes and read the AI's summary of its work and went line by line to understand the code it had implimented. Sometimes I even ran the program to see if in implimentation there were changes I would like to make.

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
