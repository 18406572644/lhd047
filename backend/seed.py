import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, engine, Base
from models import User, Building, Photo, Comment, BuildingTag, SafetyHazard, ExplorationRoute, RoutePoint
from auth import hash_password
from datetime import datetime


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        user1 = User(
            username="废墟猎人",
            email="hunter@ruins.com",
            hashed_password=hash_password("123456"),
            avatar="",
            bio="城市探险爱好者，专拍废弃建筑的孤独摄影师。"
        )
        user2 = User(
            username="遗忘见证者",
            email="witness@ruins.com",
            hashed_password=hash_password("123456"),
            avatar="",
            bio="记录被遗忘的建筑，留住城市的记忆。"
        )
        user3 = User(
            username="铁锈诗人",
            email="poet@ruins.com",
            hashed_password=hash_password("123456"),
            avatar="",
            bio="在废墟中寻找诗意的自由灵魂。"
        )
        db.add_all([user1, user2, user3])
        await db.flush()

        buildings_data = [
            {
                "title": "红星纺织厂",
                "description": "建于1958年的国营纺织厂，曾是城市的工业支柱。如今厂房内织机已被搬走，只剩下斑驳的墙面和蜘蛛网般的管道。",
                "history": "红星纺织厂成立于大跃进时期，最鼎盛时有工人3000余人。90年代国企改革后逐渐衰落，2005年彻底停产。厂区内至今保留着苏式建筑风格的厂房和办公大楼。",
                "construction_year": 1958,
                "abandonment_year": 2005,
                "building_type": "工厂",
                "address": "城东区工业大道128号",
                "latitude": 31.2304,
                "longitude": 121.4737,
                "danger_level": 2,
                "tags": ["纺织厂", "苏式建筑", "工业遗产"],
                "owner_id": 1,
                "explore_count": 156
            },
            {
                "title": "第四人民医院旧址",
                "description": "废弃的市级医院，阴森的走廊、散落的病历和生锈的手术台，是很多城市传说的发源地。",
                "history": "医院建于1972年，2010年搬迁新址后废弃。主楼6层，旁边还有一栋传染病楼。据说地下室停尸房至今还有遗留物。",
                "construction_year": 1972,
                "abandonment_year": 2010,
                "building_type": "医院",
                "address": "西城区健康路56号",
                "latitude": 31.2200,
                "longitude": 121.4500,
                "danger_level": 3,
                "tags": ["医院", "城市传说", "阴森"],
                "owner_id": 2,
                "explore_count": 289
            },
            {
                "title": "育英中学老校区",
                "description": "百年老校的废弃校区，教学楼的走廊里仿佛还能听到读书声。",
                "history": "育英中学始建于1923年，是当地最早的新式学堂之一。2015年学校整体搬迁后，老校区被遗忘在城市角落。操场上的篮球架已经锈迹斑斑。",
                "construction_year": 1923,
                "abandonment_year": 2015,
                "building_type": "学校",
                "address": "南区学府路88号",
                "latitude": 31.2100,
                "longitude": 121.4900,
                "danger_level": 2,
                "tags": ["学校", "民国建筑", "怀旧"],
                "owner_id": 1,
                "explore_count": 203
            },
            {
                "title": "国营738厂",
                "description": "神秘的军工厂，代号738。厂区很大，很多厂房被爬山虎覆盖。",
                "history": "738厂是三线建设时期的军工厂，主要生产无线电元件。80年代军转民，生产过电视机和收音机。90年代末破产倒闭。",
                "construction_year": 1966,
                "abandonment_year": 1998,
                "building_type": "工厂",
                "address": "北郊山路333号",
                "latitude": 31.2500,
                "longitude": 121.4200,
                "danger_level": 3,
                "tags": ["军工厂", "三线建设", "神秘"],
                "owner_id": 3,
                "explore_count": 342
            },
            {
                "title": "江东造船厂",
                "description": "位于江边的大型造船厂，巨大的船坞和龙门吊见证了曾经的辉煌。",
                "history": "江东造船厂建于1952年，是新中国第一批造船企业。这里造出过无数艘货轮和军舰。2008年受金融危机影响破产。",
                "construction_year": 1952,
                "abandonment_year": 2008,
                "building_type": "工厂",
                "address": "江滨路999号",
                "latitude": 31.2350,
                "longitude": 121.5100,
                "danger_level": 4,
                "tags": ["造船厂", "江边", "工业"],
                "owner_id": 2,
                "explore_count": 178
            },
            {
                "title": "圣约瑟教堂",
                "description": "哥特式风格的老教堂，彩色玻璃已经破碎，但依稀可见当年的华美。",
                "history": "教堂由法国传教士建于1898年，文革期间被用作仓库。后来归还教会，但因年久失修，加上位置偏僻，逐渐被废弃。",
                "construction_year": 1898,
                "abandonment_year": 1995,
                "building_type": "宗教",
                "address": "老城区天主堂弄15号",
                "latitude": 31.2250,
                "longitude": 121.4650,
                "danger_level": 2,
                "tags": ["教堂", "哥特式", "历史建筑"],
                "owner_id": 1,
                "explore_count": 245
            },
            {
                "title": "城市之光电影院",
                "description": "80年代最火的电影院，海报栏里还留着褪色的电影海报。",
                "history": "城市之光电影院开业于1985年，是当时全市第一家立体声影院。90年代末受电视和录像厅冲击，2002年关门大吉。",
                "construction_year": 1985,
                "abandonment_year": 2002,
                "building_type": "商业",
                "address": "市中心解放大道256号",
                "latitude": 31.2280,
                "longitude": 121.4750,
                "danger_level": 2,
                "tags": ["电影院", "80年代", "怀旧"],
                "owner_id": 3,
                "explore_count": 312
            },
            {
                "title": "北山防空洞群",
                "description": "冷战时期修建的庞大防空洞网络，像迷宫一样延伸到山体深处。",
                "history": "60年代末70年代初，为响应深挖洞号召，在北山修建了庞大的人防工程。据说里面可以容纳数万人。现在大部分入口已经被封死。",
                "construction_year": 1969,
                "abandonment_year": 1990,
                "building_type": "军事",
                "address": "北山公园后山",
                "latitude": 31.2400,
                "longitude": 121.4400,
                "danger_level": 5,
                "tags": ["防空洞", "冷战", "地下"],
                "owner_id": 2,
                "explore_count": 521
            },
        ]

        for b_data in buildings_data:
            tags = b_data.pop("tags")
            building = Building(**b_data, status="approved")
            db.add(building)
            await db.flush()

            for tag_name in tags:
                tag = BuildingTag(building_id=building.id, tag=tag_name)
                db.add(tag)

        await db.flush()

        hazards_data = [
            {"building_id": 1, "hazard_type": "结构松动", "description": "二楼部分楼板有开裂迹象", "severity": 3, "location": "二号厂房二楼"},
            {"building_id": 1, "hazard_type": "坠落物", "description": "天花板有掉落的水泥块", "severity": 2, "location": "主厂房入口"},
            {"building_id": 2, "hazard_type": "有毒物质", "description": "可能有残留的医疗废弃物", "severity": 4, "location": "传染病楼"},
            {"building_id": 4, "hazard_type": "辐射", "description": "部分车间可能有放射性物质", "severity": 5, "location": "三号车间"},
            {"building_id": 5, "hazard_type": "高空坠落", "description": "龙门吊年久失修，有零件脱落风险", "severity": 4, "location": "二号船坞"},
            {"building_id": 8, "hazard_type": "迷路风险", "description": "洞内路线复杂，容易迷路", "severity": 5, "location": "地下三层"},
            {"building_id": 8, "hazard_type": "缺氧", "description": "深层区域通风不良", "severity": 4, "location": "深处通道"},
        ]
        for h_data in hazards_data:
            hazard = SafetyHazard(**h_data)
            db.add(hazard)

        comments_data = [
            {"building_id": 1, "user_id": 2, "content": "去过一次，厂房里的大机器很震撼，记得带手电筒！", "rating": 5},
            {"building_id": 1, "user_id": 3, "content": "周末去的，门口有保安，从后面翻墙进去的。", "rating": 4},
            {"building_id": 2, "user_id": 1, "content": "真的很阴森，特别是地下室，没敢走太深。", "rating": 5},
            {"building_id": 2, "user_id": 3, "content": "假的，都是炒作，没什么好看的。", "rating": 2},
            {"building_id": 4, "user_id": 1, "content": "厂区太大了，逛了一下午都没逛完。", "rating": 5},
            {"building_id": 8, "user_id": 2, "content": "我心中的第一名！迷宫一样的地下世界，太刺激了。", "rating": 5},
            {"building_id": 8, "user_id": 3, "content": "记得带三四个光源，还有备用电池。", "rating": 5},
            {"building_id": 3, "user_id": 2, "content": "教室的黑板上还有学生写的字，瞬间穿越回学生时代。", "rating": 4},
            {"building_id": 6, "user_id": 1, "content": "彩色玻璃虽然碎了，但阳光照进来还是很美。", "rating": 5},
            {"building_id": 7, "user_id": 3, "content": "放映厅的座椅都烂了，银幕也破了，可惜。", "rating": 3},
        ]
        for c_data in comments_data:
            comment = Comment(**c_data)
            db.add(comment)

        route = ExplorationRoute(
            user_id=1,
            title="东区工业遗产一日游",
            description="一天逛完东区的三个废弃工厂，路线紧凑但都很精彩。",
            duration_minutes=480,
            difficulty=3,
            is_public=True
        )
        db.add(route)
        await db.flush()

        route_points = [
            {"route_id": route.id, "building_id": 1, "order_index": 0, "latitude": 31.2304, "longitude": 121.4737, "description": "第一站：红星纺织厂，建议停留2小时"},
            {"route_id": route.id, "building_id": 5, "order_index": 1, "latitude": 31.2350, "longitude": 121.5100, "description": "第二站：江东造船厂，江边风景不错"},
            {"route_id": route.id, "building_id": 7, "order_index": 2, "latitude": 31.2280, "longitude": 121.4750, "description": "终点站：城市之光电影院，看完正好吃饭"},
        ]
        for rp_data in route_points:
            point = RoutePoint(**rp_data)
            db.add(point)

        await db.commit()
        print("数据初始化完成！")
        print("测试账号：")
        print("  用户名: 废墟猎人, 密码: 123456")
        print("  用户名: 遗忘见证者, 密码: 123456")
        print("  用户名: 铁锈诗人, 密码: 123456")


if __name__ == "__main__":
    asyncio.run(seed_data())
