from data.config import DEBUG


def logging(type, *s):
    if type == "warn": print(f"\033[1;33m[WARNING] {';'.join(s)} \033[0m")
    if type == "info": print(f"\033[1;30m[INFO] {';'.join(s)} \033[0m")
    if type == "debug" and DEBUG: print(f"\033[1;34m[DEBUG] {';'.join(s)} \033[0m")
    if type == "error": print(f"\033[1;31m[ERROR] {';'.join(s)} \033[0m")
    if type == "success": print(f"\033[1;32m[SUCCESS] {';'.join(s)} \033[0m")

