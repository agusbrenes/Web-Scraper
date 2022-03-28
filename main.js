import got from "got";
import jsdom from "jsdom";
const { JSDOM } = jsdom;
const url = "https://crautos.com/autosusados/zonaverde/";

// const { data } = await got
// 	.post(url, {
// 		json: {
// 			hello: "world",
// 		},
// 	})
// 	.json();

// console.log(data);

const refineString = (string) => {
	const letterNumber = "/^[0-9a-zA-Z¢]+$/";
	for (var pos = 0; string[pos].match(letterNumber); pos++);
	// if (pos != string.length - 1) {
	// 	string.
	// }
};

got(url).then((res) => {
	const pageDom = new JSDOM(res.body.toString()).window.document;

	const resultsParentElement = pageDom.querySelector(".inner-page");

	const resultElements = resultsParentElement.querySelectorAll(".highbox");

	let carNumber = 0;
	resultElements.forEach((element) => {
		const carRoute = element
			.querySelector("div")
			.querySelector("a")
			.getAttribute("href");
		const carUrl = url + carRoute;
		console.log(carUrl);
		await got(carUrl).then((carPageData) => {
			const carPageDom = new JSDOM(carPageData.body.toString()).window
				.document;
			const carName = carPageDom.querySelector("h2").textContent;
			carNumber++;
			// console.log(`Carro #${carNumber}: ${carName}\n`);
			const carData = carPageDom
				.querySelector("#geninfo")
				.querySelector("table");
			const carAttributes = carData
				.querySelector("tbody")
				.querySelectorAll("tr");
			carAttributes.forEach((carAttribute) => {
				const attributePair = carAttribute.querySelectorAll("td");
				let isValue = 0;
				attributePair.forEach((pair) => {
					const letterNumber = "/^[0-9a-zA-Z]+$/";
					if (isValue) {
						let value = pair.textContent;
						value.replace("\n", " ");
						value.replace("	", " ");
						value.trim();
						// let pos = 0;
						// while (!value[pos].match(letterNumber)) {
						// 	value.replace("\n", " ");
						// 	value.trim();
						// }
						// for (var position = 0; !value[position].match(letterNumber); ) {
						// 	console.log("Aqui hay que hacerle VALUE");
						// 	//key.replace('"', "");
						// }
						// console.log("Value: " + value);
					} else {
						const key = pair.textContent;
						// console.log("Key: " + key);
					}
					isValue++;
				});
			});
			console.log(
				"--------------------------------------------------------"
			);
		});
	});
});
