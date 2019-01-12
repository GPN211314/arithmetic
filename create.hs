import System.Random
import Data.List

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

instance Show Expression where
    show (Const x) = x
    show exp@(Exp l op r) = left++" "++op++" "++right
        where left  = if leftNeedParen then "( "++(show l)++" )" else show l
              right = if rightNeedParen then "( "++(show r)++" )" else show r
              leftNeedParen = (leftPrec < opPrec) || ((leftPrec == opPrec) && (rightAssoc exp))
              rightNeedParen = (rightPrec < opPrec) || ((rightPrec == opPrec) && (leftAssoc exp))
              leftPrec  = precedence l
              rightPrec = precedence r
              opPrec    = precedence exp
              
creatRpn::Int -> StdGen -> (String, StdGen)
creatRpn 1 g = (show a, b)
  where (a, b) = randomR (1,20) g::(Int, StdGen)
creatRpn x g = ((fst $ creatRpn a g') ++ " " ++ (fst $ creatRpn b g'') ++ " " ++ op, gen''')
  where (a, gen) = randomR (1,x-1) g::(Int, StdGen)
        b = x-a
        (u, gen') = random gen::(Int, StdGen)
        g' = mkStdGen(u)
        (v, gen'') = random gen'::(Int, StdGen)
        g'' = mkStdGen(v)
        (nu, gen''') = randomR (0,4) gen''::(Int, StdGen)
        op = ["+", "-", "*", "/", "^"]!!nu 

-- 输入一个整数生成随机种子，后期准备用time做随机种子
-- 递归生成一个随机生成的表达式无限列表
creatExpLs::StdGen -> [String]
creatExpLs x = a:(creatExpLs b)
  where (y, gen) = randomR (2,11) x::(Int, StdGen)
        (a, b) = creatRpn y gen

--过滤掉表达式无限列表中的相同的表达式
sameFilter::[Expression] -> [Expression]
sameFilter (x:xs) = x : (sameFilter $ filter (/=x) xs)

buildExp :: [Expression] -> String -> [Expression]
buildExp stack x
    | not.isOp $ x = Const x : stack
    | otherwise    = Exp l x r : rest
        where r:l:rest = stack
              isOp = (`elem` ["^","*","/","+","-"])

main = do
  x <- randomIO::IO Int
  writeFile "question.txt" $ unlines.
    (map show).take 1000.sameFilter.
      (map (head.(foldl buildExp []).words)).
        creatExpLs $ mkStdGen x

