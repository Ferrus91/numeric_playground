function extendedEuclidean(a, b) {
    let x1 = 1, y1 = 0, x2 = 0, y2 = 1, r1 = a, r2 = b; 
    while (r2) {
        const q = Math.floor(r1/r2);
        xTemp = x1 - q*x2;
        yTemp = y1 - q*y2;
        rTemp = r1 - q*r2;
        x1 = x2;
        x2 = xTemp;
        y1 = y2;
        y2 = yTemp;
        r1 = r2;
        r2 = rTemp;
    }
    return { x: x1, y: y1, r: r1 }
}

function GCD(a, b) {
    const { x, y, r } = extendedEuclidean(a, b);
    return r; 
}

function GCDMultiple(...args) {
    let currentGCD = args[0];
    for (let i = 1; i < args.length; i++) {
        currentGCD = GCD(currentGCD, args[i]);
    }
    return currentGCD;
}


function LCM(a, b) {
    return a*b/GCD(a, b);
}

function LCMMultiple(...args) {
    if (args.length === 1) {
        return args[0];
    } else if (args.length === 2) {
        return LCM(args[0], args[1]);
    } else {
        const lcdNum = args.shift();
        return LCM(lcdNum, LCMMultiple(...args));
    }
}

function findMultiplicativeInverse(num, modulo) {
    const {x, y, r} = extendedEuclidean(num, modulo);
    if (r != 1) {
        return NaN;
    }
    if (x < 0) {
        return x + modulo;
    }
    return x;    
}
