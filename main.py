import sys
import lightgbm as lgb

def main():
    print(sys.version)
    print(sys.argv)
    model = lgb.LGBMClassifier(learning_rate=0.09,max_depth=-5,random_state=42)
    print(model)


if __name__ == '__main__':
    main()
