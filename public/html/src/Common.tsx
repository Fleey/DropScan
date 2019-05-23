class Common {
    public static startWith(str1: String, str2: any) {
        let reg = new RegExp("^" + str1);
        return reg.test(str2);
    }

    public static endWith(str1: String, str2: any) {
        let reg = new RegExp(str1 + '$');
        return reg.test(str2)
    }
}

export default Common
