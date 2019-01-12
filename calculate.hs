import System.Console.Haskeline
import System.Environment (getArgs)
import Data.Ratio
import Data.List
import Data.Char

--定义各符号的优先级
--由于算法中已经设置了遇"("必定压栈，")"必定出栈，故只需将其优先级设置为最小与最大即可
precedence x = case x of
                 "+" -> 2 
                 "-" -> 2 
                 "*" -> 3
                 "/" -> 3
                 "^" -> 4 
                 "(" -> 1
                 ")" -> 5


--将表达式两端加上括号，利于算法实现，并将数字与符号分开放在列表中
preprocess2 :: String -> [String]
preprocess2 xs = let ys = "(" ++ xs ++ ")"
                     isAddSpace a b = (not.isDigit $ a) || (not.isDigit $ b)
                     addSpace s acc = case acc of
                                        (z:zs) -> if isAddSpace s z
                                                   then s:' ':acc
                                                   else s:acc
                                        _      -> s:acc
                in words $ foldr addSpace [] ys 


--将**运算符全部用^替换
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


--中缀表达式转后缀表达式
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


--计算后缀表达式，为了支持分数运算，所有结果均为分数
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


--将分母为1的分数转换成整数
toString :: (Integral a, Show a) => Ratio a -> String
toString x | denominator x == 1 = show.numerator $ x
           | otherwise          = (show.numerator) x ++ "/" ++ (show.denominator $ x)

main =  getArgs >>= (\x -> case x of
                              ["-c"] -> funInput-- >>= putStrLn >> main
                                where funInput = runInputT defaultSettings loop
                                                  where loop = (getInputLine "" >>=
                                                              (\y -> case y of
                                                                       Nothing    -> return ()
                                                                       Just ""    -> return ()
                                                                       Just "exit"-> return ()
                                                                       Just "quit"-> return ()
                                                                       Just input -> (return.toString.solveRpn.toRpn.
                                                                         preprocess2.preprocess1) input >>= 
                                                                           outputStrLn >> loop
                                                              )
                                                                )
                              _    -> putStrLn "同时支持两种乘方操作\n-c  计算器交互\n-h  显示当前信息" 
                    )
