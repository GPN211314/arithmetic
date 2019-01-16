module Create
( sameFilter
, dapFilter
, buildExp
, creatExpLs
, show1
, show2
) where


import System.Random
import Data.List
import Calculate
import Data.Ratio

data Expression = Const String | Exp Expression String Expression
instance Eq Expression where
  Const a == Const b = a == b
  Const _ == Exp _ _ _ = False
  Exp _ _ _ == Const _ = False
  Exp a1 b1 c1 == Exp a2 b2 c2
    | b1 == b2 = case b1 of
                   "+" -> ((a1 == a2)&&(c1 == c2))||((a1 == c2)&&(a2 == c1))
                   "*" -> ((a1 == a2)&&(c1 == c2))||((a1 == c2)&&(a2 == c1))
                   _   -> (a1 == a2)&&(c1 == c2)
    | otherwise = False

precedence :: Expression -> Int
precedence (Const _) = 5
precedence (Exp _ op _)
    | op `elem` ["^"]     = 4
    | op `elem` ["*","/"] = 3
    | op `elem` ["+","-"] = 2
    | otherwise = 0

leftAssoc :: Expression -> Bool
leftAssoc (Const _) = False
leftAssoc (Exp _ op _) = op `notElem` ["^","*","+"]

rightAssoc :: Expression -> Bool
rightAssoc (Const _) = False
rightAssoc (Exp _ op _) = op `elem` ["^"]

--instance Show Expression where
show1 (Const x) = x
show1 exp@(Exp l op r) = left++" "++(f op)++" "++right
        where left  = if leftNeedParen then "( "++(show1 l)++" )" else show1 l
              right = if rightNeedParen then "( "++(show1 r)++" )" else show1 r
              leftNeedParen = (leftPrec < opPrec) || ((leftPrec == opPrec) && (rightAssoc exp))
              rightNeedParen = (rightPrec < opPrec) || ((rightPrec == opPrec) && (leftAssoc exp))
              leftPrec  = precedence l
              rightPrec = precedence r
              opPrec    = precedence exp
              f op = if op == "^" then "**" else op

show2 (Const x) = x
show2 exp@(Exp l op r) = left++" "++op++" "++right
        where left  = if leftNeedParen then "( "++(show2 l)++" )" else show2 l
              right = if rightNeedParen then "( "++(show2 r)++" )" else show2 r
              leftNeedParen = (leftPrec < opPrec) || ((leftPrec == opPrec) && (rightAssoc exp))
              rightNeedParen = (rightPrec < opPrec) || ((rightPrec == opPrec) && (leftAssoc exp))
              leftPrec  = precedence l
              rightPrec = precedence r
              opPrec    = precedence exp
              
creatRpn::Int -> StdGen -> (String, StdGen)
creatRpn 1 g = (show a, b)
  where (a, b) = randomR (0,20) g::(Int, StdGen)
creatRpn x g = ((fst $ creatRpn a g') ++ " " ++ (fst $ creatRpn b g'') ++ " " ++ op, gen''')
  where (a, gen) = randomR (1,x-1) g::(Int, StdGen)
        b = x-a
        (u, gen') = random gen::(Int, StdGen)
        g' = mkStdGen(u)
        (v, gen'') = random gen'::(Int, StdGen)
        g'' = mkStdGen(v)
        (nu, gen''') = randomR (0,4) gen''::(Int, StdGen)
        op = ["+", "-", "*", "/", "^"]!!nu 

-- 递归生成一个随机生成的表达式无限列表
creatExpLs::StdGen -> [String]
creatExpLs x = a:(creatExpLs b)
  where (y, gen) = randomR (2,11) x::(Int, StdGen)
        (a, b) = creatRpn y gen

--过滤掉0的0次方及0的负数次方
--过滤掉表达式无限列表中除数为零的表达式
--过滤掉过大的指数
dapFilter::[Expression] -> [Expression]
dapFilter  = filter (not.dap) 
  where dap::Expression -> Bool
        dap (Const _) = False 
        dap (Exp l x r)   | x=="/" = if dap l || dap r
                                        then True
                                        else (solveRpn.toRpn.preProcess2.preProcess1.show2) r == 0%1
                          | x=="^" = if dap l || dap r
                                        then True
                                        else if (abs.solveRpn.toRpn.preProcess2.preProcess1.show2) l > 100%1
                                                then True
                                                else if (abs.solveRpn.toRpn.preProcess2.preProcess1.show2) r > 5%1
                                                      then True
                                                      else if (denominator.solveRpn.toRpn.preProcess2.preProcess1.show2) r /= 1
                                                              then True
                                                              else if ((solveRpn.toRpn.preProcess2.preProcess1.show2) l == 0%1 &&
                                                                (solveRpn.toRpn.preProcess2.preProcess1.show2) r <= 0%1)
                                                                       then True
                                                                       else False
                          | otherwise = dap l || dap r


--过滤掉表达式无限列表中的相同的表达式
sameFilter::[Expression] -> [Expression]
sameFilter (x:xs) = x : (sameFilter $ filter (/=x) xs)

buildExp :: [Expression] -> String -> [Expression]
buildExp stack x
    | not.isOp $ x = Const x : stack
    | otherwise    = Exp l x r : rest
        where r:l:rest = stack
              isOp = (`elem` ["^","*","/","+","-"])

{-
main = do
  x <- randomIO::IO Int
  writeFile "question.txt" $ unlines.
    (map show2).take 1000.dapFilter.sameFilter.
      (map (head.(foldl buildExp []).words)).
        creatExpLs $ mkStdGen x
-}
