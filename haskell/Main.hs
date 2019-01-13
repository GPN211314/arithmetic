import System.Environment (getArgs)
import Debug.Trace
import System.IO
--import Data.List
import System.Random
import Calculate
import Create
foldl'::(IO (Int,Int,Int) -> String -> IO (Int,Int,Int)) -> IO (Int,Int,Int) ->[String] -> IO (Int,Int,Int)
foldl' _ zero [] = zero
foldl' step zero (x:xs) = traceM "asd" >> zero >>= (\m -> case m of
                                              (_,_,1) -> zero
                                              _ -> let new = (step zero x) in new `seq` foldl' step new xs
                                  )
tof expr = foldl' func (return (0,0,0)) expr >>= (\(u, v, _) -> putStrLn ("正确"++ (show u) ++ "道，共" ++ (show v) ++ "道"))
  where func s t = do
         putStr (t ++ " = ") 
         hFlush stdout
         getLine >>= (\x ->
           case x of
             "exit" -> s >>= (\(a,b,_) -> return (a,b,1))
             _ ->
              if (x == (toString.solveRpn.toRpn.preProcess2.preProcess1) t)
              then putStrLn "正确！" >> s >>= (\(a, b,_) -> return (a+1, b+1,0))
              else putStrLn "错误！" >> s >>= (\(a, b,_) -> return (a, b+1,0))
          ) 

main = do
     args <- getArgs
     x <- randomIO::IO Int
     case args of
       ["-c"] -> writeFile "question.txt" $ unlines.
         (map show).take 1000.sameFilter.
         (map (head.(foldl buildExp []).words)).
           creatExpLs $ mkStdGen x
       ["-s"] -> readFile "question.txt" >>= return.lines >>= tof
       _ -> putStrLn "同时支持两种乘方操作\n-c  生成1000道不重复的四则运算题目\n-h  显示当前信息"