# Day 1 AI Review

The calculation and grading conditions in my original solution were correct.

The main bug was that the final result section was indented inside the
`else` block. This meant that the student's information was only displayed
when the student failed. I moved the result section outside the conditional
statement so it displays for every grade.

I also stored the grade in a variable instead of printing it directly in
each condition. This made it possible to display the student's name,
average score and grade together in one organised result section.

Finally, I formatted the average score to two decimal places using `.2f`
to make the result easier to read.
