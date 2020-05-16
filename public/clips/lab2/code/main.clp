(defrule ask-age 
   (not (age ?))
   =>
   (printout t "What is your age? ")
   (bind ?age-numeric (integer (string-to-field (readline))))
   (assert (age (if (> ?age-numeric 60)
      then
         4
      else (if (> ?age-numeric 45)
            then 
               3
            else 
               1
            )
         )))
   )

(defrule ask-income 
   (not (income ?))
   =>
   (printout t "What is your income? ")
   (bind ?income-numeric (integer (string-to-field (readline))))
   (assert (income (if (> ?income-numeric 20000)
      then
         5
      else (if (> ?income-numeric 10000)
            then 
               3
            else 
               0
            )
         )))
   )

(defrule ask-status 
   (not (status ?))
   =>
   (printout t "Do you have a family? (yes/no) ")
   (bind ?family-string (readline))
   (assert (status (if (str-compare ?family-string "yes")
      then
         3
      else
         1
      )))
   )

(defrule ask-how-unhealthy-is-your-job 
   (not (how-unhealthy-is-your-job ?))
   =>
   (printout t "How unhealthy is your job? (1-5) ")
   (bind ?income-how-unhealthy-is-your-job (integer (string-to-field (readline))))
   (assert (how-unhealthy-is-your-job ?income-how-unhealthy-is-your-job))
   )

(defrule ask-illness 
   (not (illness ?))
   =>
   (printout t "Do you have any chronic diseases? (yes/no) ")
   (bind ?illness-string (readline))
   (assert (illness (if (str-compare ?illness-string "yes")
      then
         4
      else
         0
      )))
   )

(defrule run
   (age ?age)
   (income ?income)
   (status ?status)
   (illness ?illness)
   (how-unhealthy-is-your-job ?how-unhealthy-is-your-job)
   =>
   (bind ?mark (+ ?income ?age ?status ?illness ?how-unhealthy-is-your-job))
   (bind ?result (if (> ?mark 12)
        then 
           "You need an insurance. "
        else 
           "You don't need an insurance. "
      ))
   (printout t ?result "Thanks!" crlf)
   )
