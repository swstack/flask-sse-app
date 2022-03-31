## Coding test


At `https://live-test-scores.herokuapp.com/scores` you'll find a service that follows the [Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#server-sent-events) protocol. You can connect to the service using cURL:

        curl https://live-test-scores.herokuapp.com/scores

Periodically, you'll receive a JSON payload that represents a student's test score (a JavaScript number between 0 and 1), the exam number, and a student ID that uniquely identifies a student. For example:

        event: score
        data: {"exam": 3, "studentId": "foo", score: .991}

This represents that student foo received a score of `.991` on exam #3. 

Your job is to build an application that consumes this data, processes it, and provides a simple REST API that exposes the processed results. 

You may build this application in any language or stack that you prefer; we will use this project as part of your onsite interviews, so pick a language and tech stack with which you would be comfortable in a live coding session. You may use any open-source libraries or resources that you find helpful. **As part of the exercise, please replace this README file with instructions for building and running your project.** We will run your code as part of our review process.

Here's the REST API we want you to build:

1. A REST API `/students` that lists all users that have received at least one test score
2. A REST API `/students/{id}` that lists the test results for the specified student, and provides the student's average score across all exams
3. A REST API `/exams` that lists all the exams that have been recorded
4. A REST API `/exams/{number}` that lists all the results for the specified exam, and provides the average score across all students

Coding tests are often contrived, and this exercise is no exception. To the best of your ability, make your solution reflect the kind of code you'd want shipped to production. A few things we're specifically looking for:

* Well-structured, well-written, idiomatic, safe, performant code.
* Tests, reflecting the level of testing you'd expect in a production service.
* Good RESTful API design. Whatever that means to you, make sure your implementation reflects it, and be able to defend your design.
* Ecosystem understanding. Your code should demonstrate that you understand whatever ecosystem you're coding against— including project layout and organization, use of third party libraries, and build tools.

That said, we'd like you to cut some corners so we can focus on certain aspects of the problem:

* Store the results in memory instead of a persistent store. In production code, you'd never do this, of course.
* Since you're storing results in memory, you don't need to worry about the “ops” aspects of deploying your service— load balancing, high availability, deploying to a cloud provider, etc. won't be necessary.

The spec is intentionally a little underspecified. We're looking for a functional REST API that meets the criteria above, but there are no "gotchas," and there is no single "right" solution. Please use your best judgment and be prepared to explain your decisions in the on-site review.

That's it. Commit your solution to the provided GitHub repository (this one) and submit the solution using the Greenhouse link we emailed you. When you come in, we'll pair with you and walk through your solution and extend it in an interesting way.
