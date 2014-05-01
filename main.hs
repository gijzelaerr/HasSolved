{-
let w = "white"
let b = "blue"
let o = "orange"
let g = "green"
let r = "red"
let y = "yellow"

let u = "up"
let d = "down"
let f = "front"
let x = "back"
let l = "left"
let t = "right"

let colors = ("white", "blue", "orange", "green", "red", "yellow")
let sides = ("up", "down", "front", "back", "left", "right")
let axes = ("x", "y", "z")

let side_order = (u, d, f, x, l, t)

-- let positions = ( (u, f, l), (u, x, l), (u, f, t), (u, x, t), (d, f, l), (d, x, l), (d, f, t), (d, x, t), (u, f), (u, x), (u, l), (u, t), (d, f), (d, x), (d, l), (d, t)) 

-}
capital :: String -> String  
capital "" = "Empty string, whoops!"  
capital all@(x:xs) = "The first letter of " ++ all ++ " is " ++ [x]  
