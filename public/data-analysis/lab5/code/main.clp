(deftemplate monkey 
   (slot location 
      (type SYMBOL) 
      (default t1-1))
   (slot on-top-of 
      (type SYMBOL) 
      (default floor)) 
   (slot holding 
      (type SYMBOL) 
      (default blank)))

(deftemplate thing 
   (slot name 
      (type SYMBOL)
      (default ?NONE)) 
   (slot location 
      (type SYMBOL)
      (default ?NONE)) 
   (slot on-top-of 
      (type SYMBOL) 
      (default floor)))
               
(deftemplate goal-is-to 
   (slot action 
      (type SYMBOL)
      (allowed-symbols hold move on walk-to)
      (default ?NONE)) 
   (multislot arguments 
      (type SYMBOL)
      (default ?NONE)))

;;;*********************
;;;* HOLD OBJECT RULES * 
;;;*********************

(defrule use-box-to-hold ""
  (goal-is-to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ceiling))
  (not (thing (name box) (location ?place)))
  (not (goal-is-to (action move) (arguments box ?place)))
  =>
  (assert (goal-is-to (action move) (arguments box ?place))))

(defrule climb-box-to-hold ""
  (goal-is-to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ceiling))
  (thing (name box) (location ?place) (on-top-of floor))
  (monkey (on-top-of floor))
  (not (goal-is-to (action on) (arguments box)))
  =>
  (assert (goal-is-to (action on) (arguments box))))

(defrule grab-object-from-box "" 
  ?goal <- (goal-is-to (action hold) (arguments ?name))
  ?thing <- (thing (name ?name) (location ?place) 
                     (on-top-of ceiling))
  (thing (name box) (location ?place))
  ?monkey <- (monkey (location ?place) (on-top-of box) (holding blank))
  =>
  (printout t "Monkey grabs the " ?name "." crlf)
  (modify ?thing (location held) (on-top-of held))
  (modify ?monkey (holding ?name))
  (retract ?goal))

(defrule climb-to-hold ""
  (goal-is-to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ceiling))
  (thing (name box) (location ?place) (on-top-of floor))
  (monkey (on-top-of floor))
  (not (goal-is-to (action on) (arguments box)))
  =>
  (assert (goal-is-to (action on) (arguments box))))

(defrule walk-to-hold ""
  (goal-is-to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ~ceiling))
  (monkey (location ~?place))
  (not (goal-is-to (action walk-to) (arguments ?place)))
  =>
  (assert (goal-is-to (action walk-to) (arguments ?place))))

(defrule drop-to-hold ""
  (goal-is-to (action hold) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ?on))
  (monkey (location ?place) (on-top-of ?on) (holding ~blank))
  (not (goal-is-to (action hold) (arguments blank)))
  =>
  (assert (goal-is-to (action hold) (arguments blank))))

(defrule grab-object "" 
  ?goal <- (goal-is-to (action hold) (arguments ?name))
  ?thing <- (thing (name ?name) (location ?place) 
                     (on-top-of ?on))
  ?monkey <- (monkey (location ?place) (on-top-of ?on) (holding blank))
  =>
  (printout t "Monkey grabs the " ?name "." crlf)
  (modify ?thing (location held) (on-top-of held))
  (modify ?monkey (holding ?name))
  (retract ?goal))

(defrule drop-object ""  
  ?goal <- (goal-is-to (action hold) (arguments blank))
  ?monkey <- (monkey (location ?place) 
                     (on-top-of ?on) 
                     (holding ?name&~blank))
  ?thing <- (thing (name ?name))
  =>
  (printout t "Monkey drops the " ?name "." crlf)
  (modify ?monkey (holding blank))
  (modify ?thing (location ?place) (on-top-of ?on))
  (retract ?goal))

;;;*********************
;;;* MOVE OBJECT RULES * 
;;;*********************

(defrule hold-object-to-move ""  
  (goal-is-to (action move) (arguments ?obj ?place))
  (thing (name ?obj) (location ~?place))
  (monkey (holding ~?obj))
  (not (goal-is-to (action hold) (arguments ?obj)))
  =>
  (assert (goal-is-to (action hold) (arguments ?obj))))

(defrule move-object-to-place "" 
  (goal-is-to (action move) (arguments ?obj ?place))
  (monkey (location ~?place) (holding ?obj))
  (not (goal-is-to (action walk-to) (arguments ?place)))
  =>
  (assert (goal-is-to (action walk-to) (arguments ?place))))

(defrule drop-object-once-moved "" 
  ?goal <- (goal-is-to (action move) (arguments ?name ?place))
  ?monkey <- (monkey (location ?place) (holding ?obj))
  ?thing <- (thing (name ?name))
  =>
  (printout t "Monkey drops the " ?name "." crlf)
  (modify ?monkey (holding blank))
  (modify ?thing (location ?place) (on-top-of floor))
  (retract ?goal))

(defrule already-moved-object ""
  ?goal <- (goal-is-to (action move) (arguments ?obj ?place))
  (thing (name ?obj) (location ?place))
  =>
  (retract ?goal))

;;;***********************
;;;* WALK TO PLACE RULES *
;;;***********************

(defrule already-at-place "" 
  ?goal <- (goal-is-to (action walk-to) (arguments ?place))
  (monkey (location ?place))
  =>
  (retract ?goal))

(defrule get-on-floor-to-walk ""
  (goal-is-to (action walk-to) (arguments ?place))
  (monkey (location ~?place) (on-top-of ~floor))
  (not (goal-is-to (action on) (arguments floor)))
  =>
  (assert (goal-is-to (action on) (arguments floor))))

(defrule walk-holding-nothing ""
  ?goal <- (goal-is-to (action walk-to) (arguments ?place))
  ?monkey <- (monkey (location ~?place) (on-top-of floor) (holding blank))
  =>
  (printout t "Monkey walks to " ?place "." crlf)
  (modify ?monkey (location ?place))
  (retract ?goal))

(defrule walk-holding-object ""
  ?goal <- (goal-is-to (action walk-to) (arguments ?place))
  ?monkey <- (monkey (location ~?place) (on-top-of floor) (holding ?obj&~blank))
  =>
  (printout t "Monkey walks to " ?place " holding the " ?obj "." crlf)
  (modify ?monkey (location ?place))
  (retract ?goal))

;;;***********************
;;;* GET ON OBJECT RULES * 
;;;***********************

(defrule jump-onto-floor "" 
  ?goal <- (goal-is-to (action on) (arguments floor))
  ?monkey <- (monkey (on-top-of ?on&~floor))
  =>
  (printout t "Monkey jumps off the " ?on " onto the floor." crlf)
  (modify ?monkey (on-top-of floor))
  (retract ?goal))

(defrule walk-to-place-to-climb "" 
  (goal-is-to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place))
  (monkey (location ~?place))
  (not (goal-is-to (action walk-to) (arguments ?place)))
  =>
  (assert (goal-is-to (action walk-to) (arguments ?place))))

(defrule drop-to-climb "" 
  (goal-is-to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place))
  (monkey (location ?place) (holding ~blank))
  (not (goal-is-to (action hold) (arguments blank)))
  =>
  (assert (goal-is-to (action hold) (arguments blank))))

(defrule climb-indirectly "" 
  (goal-is-to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ?on))
  (monkey (location ?place) (on-top-of ~?on&~?obj) (holding blank))
  (not (goal-is-to (action on) (arguments ?on)))
  =>
  (assert (goal-is-to (action on) (arguments ?on))))

(defrule climb-directly ""  
  ?goal <- (goal-is-to (action on) (arguments ?obj))
  (thing (name ?obj) (location ?place) (on-top-of ?on))
  ?monkey <- (monkey (location ?place) (on-top-of ?on) (holding blank))
  =>
  (printout t "Monkey climbs onto the " ?obj "." crlf)
  (modify ?monkey (on-top-of ?obj))
  (retract ?goal))

(defrule already-on-object ""
  ?goal <- (goal-is-to (action on) (arguments ?obj))
  (monkey (on-top-of ?obj))
  =>
  (retract ?goal))

;;;**********************
;;;* INITIAL STATE RULE * 
;;;**********************

(defrule startup ""
  =>
  (assert (monkey (location door) (on-top-of floor) (holding blank)))
  (assert (thing (name box) (location window)))
  (assert (thing (name bananas) (location center-of-the-room) (on-top-of ceiling)))
  (assert (goal-is-to (action hold) (arguments bananas))))