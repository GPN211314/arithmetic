import System.Environment (getArgs)
import System.IO
import System.Random
import Calculate
import Create

--传统左折叠不能中断，为了实现当用户输入退出命令时退出，并统计结果，对左折叠进行了修改
foldl'::(IO (Int,Int,Int) -> String -> IO (Int,Int,Int)) -> IO (Int,Int,Int) ->[String] -> IO (Int,Int,Int)
foldl' _ zero [] = zero
foldl' step zero (x:xs) = do
  (a,b,c) <- zero
  case c of
    1 -> return (a,b,c)
    _ -> foldl' step (step (return (a,b,c)) x) xs

--判断用户输入的结果的正误，并给出最后统计结果
tof expr = (foldl' func (return (0,0,0)) expr >>= (\(u, v, _) -> putStrLn ("正确"++ (show u) ++ "道，共" ++ (show v) ++ "道")))
  where func s t = do
         (a,b,c) <- s
         putStr (t ++ " = ") 
         hFlush stdout
         x <- getLine
         case x of
             "" -> s >>= (\(a,b,_) -> return (a,b,1))
             _ -> if let y=(toString.solveRpn.toRpn.preProcess2.preProcess1) t in (y `seq` x == y)
                    then putStrLn "正确！" >> return (a+1, b+1,0) 
                    else putStrLn "错误！" >> return (a, b+1,0) 

showSelect x | x == "**" = show1
             | otherwise = show2

main = do
     args <- getArgs
     x <- randomIO::IO Int
     case args of
       ["-c"] -> putStr "请选择乘方符号（**或^）:" >> hFlush stdout >> getLine >>= (\pow -> writeFile "question.txt" $ unlines.
         (map $ showSelect pow).take 1000.sameFilter.
         (map (head.(foldl buildExp []).words)).
           creatExpLs $ mkStdGen x)
       ["-s"] -> readFile "question.txt" >>= return.lines >>= tof
       _ -> putStrLn "-c  用户选择乘方符号，生成1000道不重复的四则运算题目\n-s  用户输入结果，判断对错，输入为空时退出并给出统计结果\n-h  显示当前信息"
