;
; A simple text adventure game
; see http://www.ulisp.com/show?383X
; 

; ULOS simple object system

; Define an object
(defun object (&optional parent slots)
  (let ((obj (when parent (list (cons 'parent parent)))))
    (loop
     (when (null slots) (return obj))
     (push (cons (first slots) (second slots)) obj)
     (setq slots (cddr slots)))))

; Get the value of a slot in an object or its parents
(defun value (obj slot)
  (when (symbolp obj) (setq obj (eval obj)))
  (let ((pair (assoc slot obj)))
    (if pair (cdr pair)
           (let ((p (cdr (assoc 'parent obj))))
             (and p (value p slot))))))

; Update a slot in an object
(defun update (obj slot value)
  (when (symbolp obj) (setq obj (eval obj)))
  (let ((pair (assoc slot obj)))
    (when pair (setf (cdr pair) value))))

; Adventure game

(defparameter world 
  (object nil
          '(playing nil take #'take-anything drop #'drop-anything light #'light-anything unlock #'unlock-anything)))

(defun take-anything (obj) (format t "You can't take that.~%"))
(defun drop-anything (obj) (format t "You can't drop that.~%"))
(defun unlock-anything (obj) (format t "You can't unlock that.~%"))
(defun light-anything (obj) (format t "That's not a good idea.~%"))

(defun name-of (obj) (string-downcase obj))

; Player - starts in hall

(defparameter player (object 'world '(location hall last-location hall items nil)))

; Item class

(defparameter item (object 'world '(take #'take-item drop #'drop-item)))

(defun take-item (obj)
  (let ((where (value player 'location)))
    (cond
     ((member obj (value where 'items))
      (format t "You pick up the ~a.~%" (name-of obj))
      (update where 'items (remove obj (value where 'items)))
      (update player 'items (cons obj (value player 'items))))
     (t
      (format t "There's no ~a here.~%" (name-of obj))))))

(defun drop-item (obj)
  (let ((where (value player 'location)))
    (cond
     ((member obj (value player 'items))
      (format t "You drop the ~a.~%" (name-of obj))
      (update where 'items (cons obj (value where 'items)))
      (update player 'items (remove obj (value player 'items))))
     (t
      (format t "You're not holding any ~a.~%" (name-of obj))))))

; Items

(defparameter key (object 'item '(description "a rusty key")))

(defparameter matches (object 'item '(description "a box of matches")))

(defparameter candle 
  (object 'item '(description "a candle" light #'light-candle drop #'drop-candle lit nil)))

(defun light-candle (obj)
  (let* ((holding (value player 'items))
         (got-matches (member 'matches holding))
         (got-candle (member obj holding)))
    (cond
     ((and got-candle (value obj 'lit))
      (format t "It's already alight.~%"))
     ((and got-matches got-candle)
      (format t "You light the candle with a match, and it burns brightly.~%")
      (update obj 'lit t))
     (got-candle
      (format t "What with?~%"))
     (t
      (format t "You're not holding a candle.~%")))))

(defun drop-candle (obj)
  (cond
   ((value obj 'lit)
    (format t "It's not a good idea to drop a burning candle.~%"))
   (t
    (drop-item obj))))

; Place and exit classes

(defparameter place (object 'world))

(defparameter exit (object 'world '(locked nil move-text "go through the door")))

; Places

; Hall

(defparameter hall
  (object 'place '(description "in a large banqueting hall" 
                   exits (door hall-east hall-west hall-south) items nil)))

(defparameter door
  (object 'exit '(direction north description "an oak door" leads-to maze1 locked t
                  unlock #'unlock-door move-text "go through the oak door")))

(defun unlock-door (what)
  (let ((locked (value what 'locked))
        (got-key (member 'key (value player 'items))))
    (cond
     ((and locked got-key)
      (format t "You unlock the door with the rusty key.~%")
      (update what 'locked nil))
     (locked
      (format t "You haven't got anything to unlock it with.~%"))
     (t (format t "It's not locked.~%")))))

(defparameter hall-east
  (object 'exit '(direction east description "a small arch" leads-to garden)))

(defparameter hall-west
  (object 'exit '(direction west description "a staircase"
                  leads-to study move-text "go up the staircase")))

(defparameter hall-south
  (object 'exit '(direction south description "a large metal panel" leads-to dungeon  
                  move-text "you climb through the metal panel which swings shut behind you")))

; Study

(defparameter study
  (object 'place
          '(description "in a small study" exits (study-west) items (candle matches))))

(defparameter study-west
  (object 'exit '(direction west description "a staircase"
                  leads-to hall move-text "go down the staircase")))

; Garden

(defparameter garden
  (object 'place '(description "in a small walled garden full of beautiful flowers"
                   items (key) exits (garden-west))))

(defparameter garden-west
  (object 'exit '(direction west description "a small arch" leads-to hall)))

; Dungeon

(defparameter dungeon
  (object 'place '(description "in a dark dungeon with no windows.
                   The name 'Wes' is scratched on the wall; you wonder what his fate was" 
                   exits (dungeon-north) dark t items nil)))

(defparameter dungeon-north
  (object 'exit '(direction north description "a metal panel" leads-to hall)))

; Maze - these places all have the same description so we create maze and maze-exit classes

(defparameter maze
  (object 'place '(description "in a maze of twisty little passages, all alike")))

(defparameter maze-exit
  (object 'exit '(description "a passage" move-text "go along the passage")))

(defparameter maze1
  (object 'maze '(exits (maze1-north maze1-south maze1-east maze1-west) items nil)))

(defparameter maze1-north (object 'maze-exit '(direction north leads-to maze1)))
(defparameter maze1-south (object 'maze-exit '(direction south leads-to hall)))
(defparameter maze1-east (object 'maze-exit '(direction east leads-to maze1)))
(defparameter maze1-west (object 'maze-exit '(direction west leads-to maze2)))

(defparameter maze2
  (object 'maze '(exits (maze2-north maze2-south maze2-east maze2-west) items nil)))

(defparameter maze2-north (object 'maze-exit '(direction north leads-to maze1)))
(defparameter maze2-south (object 'maze-exit '(direction south leads-to maze2)))
(defparameter maze2-east (object 'maze-exit '(direction east leads-to maze3)))
(defparameter maze2-west (object 'maze-exit '(direction west leads-to maze2)))

(defparameter maze3
  (object 'maze '(exits (maze3-north maze3-south maze3-east maze3-west) items nil)))

(defparameter maze3-north (object 'maze-exit '(direction north leads-to maze3)))
(defparameter maze3-south
  (object 'maze-exit '(direction south leads-to beach
                       move-text "go along the passage and through a cave")))
(defparameter maze3-east (object 'maze-exit '(direction east leads-to maze2)))
(defparameter maze3-west (object 'maze-exit '(direction west leads-to maze3)))

; Beach

(defparameter beach
  (object 'place '(description "on a beautiful sandy beach next to an azure-blue sea.
                   A boat is moored nearby. Well done! You've escaped from Castle Gloom"
                   items nil)))

(defparameter beach-north
  (object 'exit '(direction north description "a cave entrance" leads-to maze3)))

; General commands

(defun take (obj) (funcall (eval (value obj 'take)) obj))
(defun drop (obj) (funcall (eval (value obj 'drop)) obj))
(defun light (obj) (funcall (eval (value obj 'light)) obj))
(defun unlock (obj) (funcall (eval (value obj 'unlock)) obj))

; Can't use "go" because it's a Common Lisp special form
(defun walk (obj)
  (let* ((where (value player 'location))
         (way (dolist (x (value where 'exits)) 
                (when (eq obj (value x 'direction)) (return x)))))
    (cond
     ((value way 'locked)
      (format t "You can't - the door seems to be locked.~%"))
     (way
      (let ((to (value way 'leads-to)))
        (format t "You ~a.~%" (value way 'move-text))
        (update player 'location to)
        (look)
        (update player 'last-location where)))
     ((eq obj 'back)
      (let ((to (value player 'last-location)))
        (format t "You go back.~%")
        (update player 'location to)
        (update player 'last-location where)
        (look)))
     (t (format t "There is no exit ~a.~%" (name-of obj))))))

(defun look ()
  (let ((where (value player 'location)))
    (cond
     ((and (value where 'dark) 
           (not (and (member 'candle (value player 'items)) (value 'candle 'lit))))
      (format t "It's totally dark and you can't see a thing.~%"))
     (t
      (format t "You are ~a.~%" (value where 'description))
      (mapc #'(lambda (exit)
                (format t "To the ~a is ~a.~%" 
                        (name-of (value exit 'direction)) (value exit 'description))) 
            (value where 'exits))
      (mapc #'(lambda (item) (format t "There is ~a here.~%" (value item 'description))) 
            (value where 'items))))))

(defun inventory ()
  (let ((items (value player 'items)))
    (cond
     (items
      (format t "You are holding: ~{~a~^, ~}.~%"
              (mapcar #'(lambda (item) (value item 'description)) items)))
     (t (format t "You are not holding anything.~%")))))

(defun adventure ()
  (unless (value world 'playing)
    (format t "Escape from Castle Gloom.~%")
    (format t "You slowly come to your senses, and then remember what happened.~%")
    (format t "You were kidnapped and brought to this castle by an evil ogre, ")
    (format t "who is asleep on a chair nearby, snoring loudly.~%")
    (update world 'playing t))
  (look)
  (loop
   (format t ": ")
   (let* ((line (read-line))
          (verb (read-from-string line))
          (sp (dotimes (c (length line)) (when (eq (char line c) #\space) (return c)))))
     (terpri)
     (case verb
       ; Single-word commands
       ((look inventory) (funcall verb))
       ((~ quit) (return))
       ; Two-word commands
       ((go take drop light unlock)
        (when sp
          (let ((noun (read-from-string (subseq line (1+ sp)))))
          (cond
           ((eq verb 'go) (funcall #'walk noun))
           ((not (boundp noun))
            (format t "I don't understand.~%"))
           (t (funcall verb noun))))))
       (t (format t "~%I don't know how to do that.~%"))))))