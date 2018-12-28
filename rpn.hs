import System.Environment (getArgs)
import Data.Ratio
import Data.List
import Data.Char

precedence x = case x of
                 "+" -> 2 
                 "-" -> 2 
                 "*" -> 3
                 "/" -> 3
                 "^" -> 4 
                 "(" -> 1
                 ")" -> 5


preprocess2 :: String -> [String]
preprocess2 xs = let ys = "(" ++ xs ++ ")"
                     isAddSpace a b = (not.isDigit $ a) || (not.isDigit $ b)
                     addSpace s acc = case acc of
                                        (z:zs) -> if isAddSpace s z
                                                   then s:' ':acc
                                                   else s:acc
                                        _      -> s:acc
                in words $ foldr addSpace [] ys 


preprocess1 :: String -> String
preprocess1 xs = foldr funDel [] $ zip ys (map ("*^" `isPrefixOf`) $ tails ys)
              where ys = foldr funInst [] $ zip xs (False:(init (map ("**" `isPrefixOf`) $ tails xs)))
                            where funInst (x, valBool) acc =
                                          case valBool of
                                              True -> '^':acc
                                              _    -> x:acc
                    funDel (x, valBool) acc = case valBool of
                                                True -> acc
                                                _    -> x:acc

toRpn :: [String] -> [String]
toRpn xs = reverse.fst $ foldl' infix2rpn ([],[]) xs
              where infix2rpn (nums, ops) x = 
                     if (isOp x) 
                      then popStack nums ops 
                      else pushStack 
                        where popStack as bs = 
                                case bs of
                                  b:rest -> case x of
                                              "(" -> (as,(x:bs))
                                              ")" -> if b == "("
                                                        then (as, rest)
                                                        else popStack (b:as) rest
                                              _ -> if ((precedence x) <= (precedence b)) && (x /= "^"||b /= "^")
                                                      then popStack (b:as) rest
                                                      else (as ,(x:bs))
                                  _      -> (as ,(x:bs))
                              pushStack = ((x:nums), ops)
                              isOp = (`elem` ["+", "-", "*", "/", "^", "(", ")"])


solveRpn :: (Read a, Show a, Integral a) => [String] -> Ratio a
solveRpn = head.foldl' func []
  where func :: (Read a, Integral a) => [Ratio a] -> String -> [Ratio a]
        func xs par=case xs of
                      (x:y:ys) -> case par of
                                    "*" -> (y * x):ys
                                    "-" -> (y - x):ys
                                    "/" -> (y / x):ys
                                    "^" -> (y ^^ (round x)):ys
                                    "+" -> (y + x):ys
                                    _   -> (fromIntegral.read) par:xs
                      _   -> (fromIntegral.read) par:xs

toString :: (Integral a, Show a) => Ratio a -> String
toString x | denominator x == 1 = show.numerator $ x
           | otherwise          = (show.numerator) x ++ "/" ++ (show.denominator $ x)

main =  getArgs >>= (\x -> case x of
                              ["-c"] -> getLine >>= 
                                (return.toString.solveRpn.toRpn.
                                  preprocess2.preprocess1) >>= 
                                  putStrLn >> main
                              _    -> putStrLn "同时支持两种乘方操作\n-c  计算器交互\n-h 显示当前信息" >> return ()
                   )
