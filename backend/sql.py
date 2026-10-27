sql_schema = """
CREATE TABLE `orders` (
        `order_id` int NOT NULL AUTO_INCREMENT,
        `user_id` int NOT NULL,
        `product_id` int NOT NULL,
        `quantity` int NOT NULL,
        `price` decimal(10,2) NOT NULL COMMENT 'Unit price at purchase',
        `status` enum('pending','confirmed','shipped','delivered','cancelled','refunded') NOT NULL,
        `payment_mode` enum('upi','credit_card','debit_card','net_banking','cod') NOT NULL,
        `order_placed_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`order_id`),
        KEY `user_id` (`user_id`),
        KEY `product_id` (`product_id`),
        CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
        CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`),
        CONSTRAINT `orders_chk_1` CHECK ((`quantity` > 0)),
        CONSTRAINT `orders_chk_2` CHECK ((`price` >= 0))
    ) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    CREATE TABLE `products` (
        `product_id` int NOT NULL AUTO_INCREMENT,
        `title` varchar(200) NOT NULL,
        `price` decimal(10,2) NOT NULL,
        `is_stock_available` tinyint(1) NOT NULL DEFAULT '1',
        PRIMARY KEY (`product_id`),
        CONSTRAINT `products_chk_1` CHECK ((`price` >= 0))
    ) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

    CREATE TABLE `users` (
        `user_id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(100) NOT NULL,
        `email` varchar(150) NOT NULL,
        `mobile` varchar(20) NOT NULL,
        `utm_source` varchar(50) DEFAULT NULL,
        `is_email_verified` tinyint(1) NOT NULL DEFAULT '0',
        `account_created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`user_id`),
        UNIQUE KEY `email` (`email`)
    ) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


"""